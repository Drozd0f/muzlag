from dataclasses import dataclass


@dataclass
class PlaylistModel:
    playlist_id: int
    member_id: int
    name: str

    @property
    def tag_member(self) -> str:
        return f'<@{self.member_id}>'
