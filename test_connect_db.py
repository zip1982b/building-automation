import asyncio
import aiopg

dsn = 'dbname=mydb user=zip1982b password=zhan99999 host=192.168.0.100'


async def test_select():
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM users")
                #ret = await cur.fetchall()
                ret = await cur.fetchone()
                print(ret)
                #ret = []
                #async for row in cur:
                    #ret.append(row)
                    #print(row)
                #assert ret == [(1,)]

    print("ALL DONE")


loop = asyncio.get_event_loop()
loop.run_until_complete(test_select())



