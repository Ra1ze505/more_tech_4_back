import copy
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel, parse_obj_as
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlmodel import SQLModel
from starlette import status

from src.data.db.db import Database


class BaseRepo:

    model: SQLModel
    query: Select
    schema: BaseModel
    out_schema: BaseModel

    def __init__(self, db: Database):
        self.db = db

    def get_query(self) -> Select:
        query = self.query if self.query is not None else select(self.model)
        return copy.copy(query)

    @property
    def session(self) -> AsyncSession:
        return self.db.session

    async def get_all(self):
        q = self.get_query()
        return (await self.session.execute(q)).scalars().all()

    async def get_one(self, field_name: str, field_value: Any):
        q = self.get_query().where(getattr(self.model, field_name) == field_value)
        return (await self.session.execute(q)).scalars().one()

    async def create(self, data: dict):
        obj = self.model(**data)
        self.session.add(obj)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Object already exists"
            )
        q = select(self.model).where(self.model.id == obj.id)
        obj = (await self.session.execute(q)).scalars().one()
        return parse_obj_as(self.out_schema, obj)

    async def update(self, data: dict):
        q = select(self.model).where(self.model.id == data.get("id"))
        result = await self.session.execute(q)
        obj = result.unique().scalars().one()

        for key, val in data.items():
            setattr(obj, key, val)

        self.session.add(obj)
        await self.session.commit()

        return parse_obj_as(self.out_schema, obj)
