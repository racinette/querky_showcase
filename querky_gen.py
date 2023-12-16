import asyncio

from querky.presets.asyncpg import generate

from querky_def import qrk
import sql
from env import CONNECTION_STRING


if __name__ == "__main__":
    asyncio.run(generate(qrk, CONNECTION_STRING, base_modules=(sql, )))
