import asyncio

import asyncpg

from env import CONNECTION_STRING

# import queries
from sql.queries.example2 import insert_account, insert_post, insert_post_comment
from sql.queries.example import get_account_referrer, select_last_post_comments


async def main():
    conn = await asyncpg.connect(CONNECTION_STRING)

    try:
        async with conn.transaction():
            account_id = await insert_account(
                conn,
                first_name="Andrei",
                last_name="Karavatski",
                balance=1000,
                phone_number=None,
                username="racinette"
            )

            referred_account_id = await insert_account(
                conn,
                first_name="Max",
                last_name="K.",
                balance=2000,
                phone_number=None,
                username="maxbot",
                referred_by_account_id=account_id
            )

            post_id = await insert_post(
                conn,
                poster_id=account_id,
                message="Hello, World!"
            )

            await insert_post_comment(
                conn,
                post_id=post_id,
                commenter_id=referred_account_id,
                message="What's up?"
            )

            first_account = await get_account_referrer(conn, referred_account_id)
            print(first_account.first_name, first_account.last_name)

            comments = await select_last_post_comments(conn, post_id=post_id, limit=3)
            print(comments)
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
