"""Module with ROLE CRUD realisation"""

from .base import CRUDBase
from app.models import Role
from app.schemas.role import RoleCreate, RoleUpdate, RoleBase, RoleList


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    """A class that inherits the base CRUD class
    to perform CRUD operations for the ROLE model"""
    ...


ROLE = CRUDRole(Role, RoleBase, RoleList)
