import asyncpg
import asyncio

async def check_connection():
    try:
        conn = await asyncpg.connect(
            user="postgres", password="cyber",
            database="chatsystem", host="localhost",
            timeout=3
        )

        await conn.close()
        return True

    except (asyncpg.exceptions.PostgresError, OSError) as e:
        print(f"Connection faile: {e}")
        return False


if __name__ == "__main__":
    result = asyncio.run(check_connection())