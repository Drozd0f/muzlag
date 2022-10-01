import logging
import typing as t
from sqlite3 import IntegrityError

import aiosqlite
from nextcord import Member

from bot.config import DBConfig
from bot.src.yt_search import YoutubeSearch
from bot.errors.playlist import PlaylistNameExists, SongInPlaylistExists
from bot.database.models.playlist import PlaylistModel
from bot.database.models.songs import SongModel
from bot.database.models.paginator import PaginatorModel


log = logging.getLogger(__name__)


def get_query(query_dir: str, query_name: str) -> t.Optional[str]:
    try:
        with open(f'{query_dir}/{query_name}.sql', mode='r') as f:
            return f.read()
    except FileNotFoundError:
        log.exception(f'Query {query_name}.sql not found in {query_dir}')


async def create_playlist(member: Member, playlist_name: str) -> t.Optional[PlaylistModel]:
    async with aiosqlite.connect(DBConfig.path) as conn:
        try:
            cursor = await conn.cursor()
            await cursor.execute(
                get_query(DBConfig.queries_dir, 'create_playlist'),
                {
                    'member_id': member.id,
                    'name': playlist_name
                }
            )
            row = await cursor.fetchone()
            await conn.commit()
            await cursor.close()
        except IntegrityError as exc:
            logging.error(exc)
            raise PlaylistNameExists
    if row is not None:
        return PlaylistModel(*row)


async def create_song(yt_search: YoutubeSearch) -> SongModel:
    async with aiosqlite.connect(DBConfig.path) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            get_query(DBConfig.queries_dir, 'create_song'),
            {
                'video_id': yt_search.video_id,
                'title': yt_search.title,
                'url': yt_search.url,
                'start_time': yt_search.start_time
            }
        )
        await conn.commit()
        await cursor.close()
    return SongModel(
        song_id=yt_search.video_id,
        title=yt_search.title,
        url=yt_search.url,
        start_time=yt_search.start_time
    )


async def get_member_playlists(member: Member, paginator: PaginatorModel) -> t.Optional[t.List[PlaylistModel]]:
    async with aiosqlite.connect(DBConfig.path) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            get_query(DBConfig.queries_dir, 'get_member_playlists'),
            {
                'member_id': member.id,
                'offset': paginator.offset,
                'limit': paginator.limit
            }
        )
        rows = await cursor.fetchall()
        await cursor.close()
    if rows is not None:
        return [PlaylistModel(*row) for row in rows]


async def get_member_count_playlists(member: Member) -> int:
    async with aiosqlite.connect(DBConfig.path) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            get_query(DBConfig.queries_dir, 'get_member_count_playlists'),
            {
                'member_id': member.id,
            }
        )
        count, = await cursor.fetchone()
        await cursor.close()
    return count


async def get_all_playlists(paginator: PaginatorModel) -> t.Optional[t.List[PlaylistModel]]:
    async with aiosqlite.connect(DBConfig.path) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            get_query(DBConfig.queries_dir, 'get_all_playlists'),
            {
                'offset': paginator.offset,
                'limit': paginator.limit
            }
        )
        rows = await cursor.fetchall()
        await cursor.close()
    if rows is not None:
        return [PlaylistModel(*row) for row in rows]


async def get_count_playlists() -> int:
    async with aiosqlite.connect(DBConfig.path) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            get_query(DBConfig.queries_dir, 'get_count_playlists'),
        )
        count, = await cursor.fetchone()
        await cursor.close()
    return count


async def get_playlist_songs(playlist: PlaylistModel, paginator: PaginatorModel) -> t.Optional[t.List[SongModel]]:
    async with aiosqlite.connect(DBConfig.path) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            get_query(DBConfig.queries_dir, 'get_playlist_songs'),
            {
                'playlist_id': playlist.playlist_id,
                'offset': paginator.offset,
                'limit': paginator.limit
            }
        )
        rows = await cursor.fetchall()
        await cursor.close()
    if rows is not None:
        return [SongModel(*row) for row in rows]


async def get_song_in_playlist(playlist: PlaylistModel, song: SongModel) -> SongModel:
    async with aiosqlite.connect(DBConfig.path) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            get_query(DBConfig.queries_dir, 'get_song_in_playlist'),
            {
                'playlist_id': playlist.playlist_id,
                'song_id': song.song_id
            }
        )
        row = await cursor.fetchone()
        await cursor.close()
    if row is not None:
        return SongModel(*row)


async def get_count_songs_in_playlists(playlist: PlaylistModel) -> int:
    async with aiosqlite.connect(DBConfig.path) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            get_query(DBConfig.queries_dir, 'get_count_songs_in_playlists'),
            {
                'playlist_id': playlist.playlist_id
            }
        )
        count, = await cursor.fetchone()
        await cursor.close()
    return count


async def update_playlist(playlist: PlaylistModel, song: SongModel):
    if await get_song_in_playlist(playlist, song):
        raise SongInPlaylistExists
    async with aiosqlite.connect(DBConfig.path) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            get_query(DBConfig.queries_dir, 'update_playlist'),
            {
                'playlist_id': playlist.playlist_id,
                'song_id': song.song_id
            }
        )
        await conn.commit()
        await cursor.close()
