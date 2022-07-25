from __future__ import annotations
from asyncio import Queue, QueueEmpty
from dataclasses import dataclass

import typing as t


@dataclass
class ModQueue:
    queue: Queue = Queue()
    is_repeat: bool = False
    current_song: t.Optional[str] = None


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
        await self.__queues[channel_id].queue.put(song_url)

    def get(self, channel_id: int) -> str:
        if channel_id not in self.__queues:
            self.drop(channel_id)
            raise QueueEmpty
        if not self.__queues[channel_id].is_repeat:
            self.__queues[channel_id].current_song = self.__queues[channel_id].queue.get_nowait()
        return self.__queues[channel_id].current_song

    def switch_repeat(self, channel_id: int):
        if channel_id not in self.__queues:
            self.drop(channel_id)
            raise QueueEmpty
        self.__queues[channel_id].is_repeat = not self.__queues[channel_id].is_repeat

    def skip(self, channel_id: int, count: int):
        for _ in range(count):
            self.__queues[channel_id].queue.get_nowait()
        if queue := self.__queues.get(channel_id).queue:
            queue.task_done()

    def drop(self, channel_id: int):
        if channel_id in self.__queues:
            del(self.__queues[channel_id])

    def is_repeat(self, channel_id: int) -> bool:
        return self.__queues[channel_id].is_repeat

    def __contains__(self, channel_id: int) -> bool:
        return channel_id in self.__queues
