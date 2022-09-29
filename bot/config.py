import os
from enum import Enum
from dataclasses import dataclass
from pathlib import Path


class Envs(Enum):
    PROD = 'prod'
    DEV = 'dev'
    TEST = 'test'


@dataclass
class Config:
    prefix = os.getenv('PREFIX')
    token = os.getenv('TOKEN')
    base_dir = Path(__file__).parent.parent.resolve()
    env = Envs(os.getenv('ENV')).value
    playlist_limit = 5


@dataclass
class DBConfig:
    name = os.getenv('DB_NAME', 'muzlag')
    path = f'{Config.base_dir}/db/{name}.db'
    database_dir = f'{Config.base_dir}/bot/database'
    queries_dir = f'{database_dir}/queries'
    migrations_dir = f'{database_dir}/migrations'
