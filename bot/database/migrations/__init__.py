import logging
import re
import typing as t
from pathlib import Path
from sqlite3 import OperationalError

import aiosqlite

from bot.database import get_query
from bot.config import DBConfig


log = logging.getLogger(__name__)


class Migrator:
    @classmethod
    async def _create_scheme(cls):
        async with aiosqlite.connect(DBConfig.path) as conn:
            cursor = await conn.cursor()
            await cursor.executescript(get_query(DBConfig.migrations_dir, 'create_scheme.up'))
            await cursor.close()

        if await cls._get_current_version() is None:
            async with aiosqlite.connect(DBConfig.path) as conn:
                cursor = await conn.cursor()
                await cursor.executescript(get_query(DBConfig.queries_dir, 'create_base_migration_value'))
                await cursor.close()

    @staticmethod
    def _get_migration_paths() -> list[Path]:
        return sorted(list(Path(DBConfig.migrations_dir).glob('[0-9]*_*.up.sql')))

    @staticmethod
    def _parse_migration_number(name_migrate: str) -> int:
        return int(re.findall(r'\d+', name_migrate)[0])

    @staticmethod
    async def _get_current_version() -> t.Optional[int]:
        async with aiosqlite.connect(DBConfig.path) as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                get_query(DBConfig.queries_dir, 'get_current_version_migrations')
            )
            res = await cursor.fetchone()
            await cursor.close()
        if res:
            return res[0]

    @staticmethod
    async def _apply_migration(migration_name: str):
        async with aiosqlite.connect(DBConfig.path) as conn:
            cursor = await conn.cursor()
            await cursor.execute('BEGIN')
            queries = get_query(DBConfig.migrations_dir, migration_name).split(';')
            try:
                for query in queries:
                    await cursor.execute(query)
                await cursor.execute('COMMIT')
            except OperationalError as exc:
                await cursor.execute('ROLLBACK')
                logging.error(exc)
                raise exc
            await cursor.close()

    @staticmethod
    async def _update_migration_schema(current_version: int, is_dirt: bool):
        async with aiosqlite.connect(DBConfig.path) as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                get_query(DBConfig.queries_dir, 'update_migration_schema'),
                {
                    'current_version': current_version,
                    'is_dirt': is_dirt
                }
            )
            await conn.commit()
            await cursor.close()

    @classmethod
    async def start(cls):
        await cls._create_scheme()
        migrations_path = cls._get_migration_paths()
        current_version = await cls._get_current_version()
        is_dirt = False
        try:
            for migrate_path in migrations_path:
                migration_version = cls._parse_migration_number(migrate_path.stem)
                if migration_version > current_version:
                    current_version = migration_version
                    log.info(f'Try apply migration {migrate_path.stem}')
                    await cls._apply_migration(migrate_path.stem)
                    log.info(f'Migration {migrate_path.stem} has been applied')
        except Exception as e:
            is_dirt = True
            log.exception(f'Dirty version - {current_version}')
            raise e
        finally:
            await cls._update_migration_schema(current_version, is_dirt)
