import asyncio
import aiopg

dsn = 'dbname=mydb user=zip1982b password=zhan99999 host=localhost'


async def test_select():
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM users")
                res = cur.statusmessage
                print(res)

    print("ALL DONE")


loop = asyncio.get_event_loop()
loop.run_until_complete(test_select())



