

from typing import List, Type


class BaseRole:
    role_name: str
    lower_roles: List["BaseRole"] | None = None

    def __new__(cls):
        raise Exception("Refuse to create instance of the BaseRole!")

    @classmethod
    def get_roles(cls) -> List[Type["BaseRole"]]:
        return cls.__subclasses__()


class UserRole(BaseRole):
    role_name = "USER"


class ManagerRole(BaseRole):
    role_name = "MANAGER"
    lower_roles = [UserRole]


class AdminRole(BaseRole):
    role_name = "ADMIN"
    lower_roles = [UserRole, ManagerRole]


class RoleManager:
    _base_role = BaseRole

    def __init__(self) -> None:
        self.all_roles = {r.role_name: r for r in self._base_role.get_roles()}

    def validate_role(self, user_role: str, required_role: str, role_objects: List[BaseRole] | None = None) -> bool:
        user_role = user_role.upper()
        required_role = required_role.upper()
        if user_role == required_role:
            return True
        elif not self.all_roles.get(required_role):
            raise Exception("Required role das not exist")

        role_objects = [self.all_roles.get(user_role)] if not role_objects else role_objects
        for role_object in role_objects:
            if not role_object or role_object.role_name != required_role and not role_object.lower_roles:
                return False
            elif role_object.role_name == required_role:
                return True
            else:
                return self.validate_role(user_role, required_role, role_object.lower_roles)
