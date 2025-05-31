import os, asyncpg, glob, asyncio
DB_URL = os.getenv("DATABASE_URL")

async def run():
    conn = await asyncpg.connect(DB_URL)
    await conn.execute("CREATE TABLE IF NOT EXISTS _migrations(filename text primary key);")
    done = {r[0] for r in await conn.fetch("SELECT filename FROM _migrations")}
    for path in sorted(glob.glob("migrations/*.sql")):
        name = os.path.basename(path)
        if name in done:
            continue
        print(f"applying {name}")
        await conn.execute(open(path).read())
        await conn.execute("INSERT INTO _migrations(filename) VALUES($1)", name)
    await conn.close()
if __name__ == "__main__":
    asyncio.run(run())
