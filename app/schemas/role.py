"""Module with role pydentic schemas"""

from typing import List

from pydantic import BaseModel, constr


class RoleBase(BaseModel):
    """Base schema"""
    name: constr(max_length=20)

    class Config:
        """Configuration class"""
        orm_mode = True


class RoleCreate(RoleBase):
    """Create schema"""


class RoleUpdate(RoleBase):
    """Update schema"""


class RoleInDBBase(RoleBase):
    """Database schema"""
    role_id: int


class RoleList(BaseModel):
    """List of base schema objects schema"""
    __root__: List[RoleBase]

    class Config:
        """Configuration class"""
        orm_mode = True
