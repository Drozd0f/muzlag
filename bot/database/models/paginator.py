from dataclasses import dataclass

from bot.config import Config


@dataclass
class PaginatorModel:
    page: int
    limit: int = Config.playlist_limit

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
