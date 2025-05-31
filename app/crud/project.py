# app/crud/project.py
from typing import List
from app.db.connection import get_pool
from app.schemas.project import ProjectCreate, Project

async def create_project(data: ProjectCreate, user_id: str) -> Project:
    pool = await get_pool()
    async with pool.acquire() as con:
        row = await con.fetchrow(
            "INSERT INTO hub_project(bk_project, load_dts, rec_src) VALUES($1, now(), 'api') RETURNING hk_project",
            data.name,
        )
        return Project(id=row[0], **data.dict())
