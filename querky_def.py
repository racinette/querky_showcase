import os
from querky.presets.asyncpg import use_preset


qrk = use_preset(os.path.dirname(__file__), type_factory='dataclass+slots')
