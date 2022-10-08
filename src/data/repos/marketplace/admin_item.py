from sqlalchemy import select

from src.data.models import AdminItem
from src.data.repos.base import BaseRepo
from src.domain.marketplace.admin_item.dto.base import AdminItemBaseSchema, AdminItemOutSchema


class AdminItemRepo(BaseRepo):
    model = AdminItem
    query = select(AdminItem)
    schema = AdminItemBaseSchema
    out_schema = AdminItemOutSchema
