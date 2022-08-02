from __future__ import annotations
import typing as t
from asyncio import Queue, QueueEmpty
from collections import deque

from src.players import player_factory


class ModQueue(Queue):
    __is_repeat: bool = False
    __current_song: t.Optional[str] = None

    @property
    def queue(self) -> deque:
        return self._queue

    @property
    def current_song(self) -> str:
        return self.__current_song

    @current_song.setter
    def current_song(self, song: str):
        self.__current_song = song

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

    async def push(self, channel_id: int, song_url: str):
        if channel_id not in self.__queues:
            self.__queues[channel_id] = ModQueue()
        await self.__queues[channel_id].put(song_url)

    def get(self, channel_id: int) -> str:
        if channel_id not in self.__queues:
            self.drop(channel_id)
            raise QueueEmpty
        if not self.__queues[channel_id].is_repeat:
            self.__queues[channel_id].current_song = self.__queues[channel_id].get_nowait()
        return self.__queues[channel_id].current_song

    def switch_repeat(self, channel_id: int):
        if channel_id not in self.__queues:
            self.drop(channel_id)
            raise QueueEmpty
        self.__queues[channel_id].is_repeat = not self.__queues[channel_id].is_repeat

    def show_queue(self, channel_id: int):
        if channel_id not in self.__queues:
            self.drop(channel_id)
            raise QueueEmpty
        return [player_factory(url).title for url in self.__queues[channel_id].queue]

    def skip(self, channel_id: int, count: int):
        for _ in range(count):
            self.__queues[channel_id].get_nowait()
        if queue := self.__queues.get(channel_id):
            queue.task_done()

    def drop(self, channel_id: int):
        if channel_id in self.__queues:
            del self.__queues[channel_id]

    def is_repeat(self, channel_id: int) -> bool:
        return self.__queues[channel_id].is_repeat

    def __contains__(self, channel_id: int) -> bool:
        return channel_id in self.__queues
