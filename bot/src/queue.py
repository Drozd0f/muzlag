from __future__ import annotations

import typing as t
from asyncio import Queue, QueueEmpty
from collections import deque

from bot.src.players.base import BasePlayer


class ModQueue(Queue):
    __is_repeat: bool = False
    __current_player: t.Optional[BasePlayer] = None

    @property
    def queue(self) -> deque:
        return self._queue

    @property
    def current_player(self) -> BasePlayer:
        return self.__current_player

    @current_player.setter
    def current_player(self, player: BasePlayer):
        self.__current_player = player

    @property
    def is_repeat(self) -> bool:
        return self.__is_repeat

    @is_repeat.setter
    def is_repeat(self, value: bool):
        self.__is_repeat = value


class MuzlagQueue:
    obj = None
    __queues: t.Dict[int, ModQueue] = {}

    def __new__(cls: MuzlagQueue, *args, **kwargs) -> MuzlagQueue:
        if cls.obj:
            return cls.obj
        cls.obj = super().__new__(cls, *args, **kwargs)
        return cls.obj

    async def push(self, channel_id: int, player: BasePlayer):
        if channel_id not in self.__queues:
            self.__queues[channel_id] = ModQueue()
        await self.__queues[channel_id].put(player)

    def get(self, channel_id: int) -> BasePlayer:
        if channel_id not in self.__queues:
            self.drop(channel_id)
            raise QueueEmpty
        if not self.__queues[channel_id].is_repeat:
            self.__queues[channel_id].current_player = self.__queues[channel_id].get_nowait()
        return self.__queues[channel_id].current_player

    def switch_repeat(self, channel_id: int):
        if channel_id not in self.__queues:
            self.drop(channel_id)
            raise QueueEmpty
        self.__queues[channel_id].is_repeat = not self.__queues[channel_id].is_repeat

    def show_queue(self, channel_id: int) -> str:
        if channel_id not in self.__queues:
            self.drop(channel_id)
            raise QueueEmpty

        queue = f'1. {self.__queues[channel_id].current_player.title} \n'
        if self.is_repeat(channel_id):
            queue = f'1. {self.__queues[channel_id].current_player.title}  :repeat:\n'

        for idx, player in enumerate(self.__queues[channel_id].queue):
            queue += f'{idx + 2}. {player.title} \n'
        return queue

    def skip(self, channel_id: int, count: int = 1):
        if channel_id not in self.__queues:
            self.drop(channel_id)
            raise QueueEmpty

        if count == 1:
            if self.is_repeat(channel_id):
                self.switch_repeat(channel_id)
            self.__queues[channel_id].current_player = None
        else:
            for _ in range(count - 1):
                self.__queues[channel_id].get_nowait()

        if not len(self.__queues[channel_id].queue):
            self.__queues.get(channel_id).task_done()

    def drop(self, channel_id: int):
        if channel_id in self.__queues:
            del self.__queues[channel_id]
        raise QueueEmpty

    def current_song(self, channel_id: int) -> str:
        return self.__queues[channel_id].current_player.title

    def is_repeat(self, channel_id: int) -> bool:
        return self.__queues[channel_id].is_repeat

    def __contains__(self, channel_id: int) -> bool:
        return channel_id in self.__queues
