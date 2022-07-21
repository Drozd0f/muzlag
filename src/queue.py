from __future__ import annotations
from asyncio import Queue, QueueEmpty

import typing as t


class MuzlagQueue:
    obj = None
    __queues: t.Dict[int, Queue] = {}

    def __new__(cls: MuzlagQueue, *args, **kwargs) -> MuzlagQueue:
        if cls.obj:
            return cls.obj
        cls.obj = super().__new__(cls, *args, **kwargs)
        return cls.obj

    async def push(self, channel_id: int, song_url: str):
        if channel_id not in self.__queues:
            self.__queues[channel_id] = Queue()
        await self.__queues[channel_id].put(song_url)

    def get(self, channel_id: int) -> str:
        if channel_id not in self.__queues:
            self.drop(channel_id)
            raise QueueEmpty
        return self.__queues[channel_id].get_nowait()

    def skip(self, channel_id: int):
        if queues := self.__queues.get(channel_id):
            queues.task_done()

    def drop(self, channel_id: int):
        if channel_id in self.__queues:
            del(self.__queues[channel_id])

    def __contains__(self, channel_id: int) -> bool:
        return channel_id in self.__queues
