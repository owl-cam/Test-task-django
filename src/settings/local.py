import os
from pathlib import Path

import environ

environ.Env.read_env(
    os.path.join(Path(__file__).resolve().parent.parent.parent, ".env")
)

from .base import *
