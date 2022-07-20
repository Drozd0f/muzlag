from asyncio import Queue, QueueEmpty

import typing as t


class Player:
    obj = None
    __queues: t.Dict[int, Queue] = {}

    def __new__(cls, *args, **kwargs):
        if obj := cls.obj:
            return obj

        cls.obj = super().__new__(cls, *args, **kwargs)
        return cls.obj

    async def push(self, channel_id: int, song_url: str):
        if channel_id not in self.__queues:
            self.__queues[channel_id] = Queue()

        await self.__queues[channel_id].put(song_url)

    def get(self, channe_id: int):
        if channe_id not in self.__queues:
            raise QueueEmpty

        return self.__queues[channe_id].get_nowait()

    def drop(self, channel_id: int):
        if channel_id in self.__queues:
            del(self.__queues[channel_id])
