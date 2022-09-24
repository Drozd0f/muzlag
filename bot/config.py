import os
from dataclasses import dataclass
from pathlib import Path


BASE_PATH = Path(__file__).parent.parent.resolve()


@dataclass
class Config:
    prefix = os.getenv('PREFIX')
    token = os.getenv('TOKEN')
