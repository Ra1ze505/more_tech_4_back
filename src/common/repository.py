import copy
from typing import Any

from fastapi import HTTPException
from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from starlette import status

from src.common.db import Base, Database
from src.common.schema import BaseSchema


class BaseRepo:

    model: Base
    query: Select
    schema: BaseSchema
    out_schema: BaseSchema

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
        objects = (await self.session.execute(q)).scalars().all()
        return parse_obj_as(list[self.out_schema], objects)

    async def get_one(self, field_value: Any, field_name: str = "id"):
        q = self.get_query().where(getattr(self.model, field_name) == field_value)
        try:
            obj = (await self.session.execute(q)).scalars().one()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__tablename__} object not found",
            )
        return parse_obj_as(self.out_schema, obj)

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

        return parse_obj_as(self.schema, obj)
