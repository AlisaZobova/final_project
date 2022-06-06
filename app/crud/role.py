"""Module with ROLE CRUD realisation"""

from .base import CRUDBase
from app.models import Role
from app.schemas.role import RoleCreate, RoleUpdate, RoleBase, RoleList
from app.models.db_init import DATABASE


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the ROLE model"""
    def remove(self, database: DATABASE.session, *, record_id: int):
        """The role table will not have a delete method"""


ROLE = CRUDRole(Role, RoleBase, RoleList)
