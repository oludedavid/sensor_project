from enum import Enum as PyEnum

class RoleEnum(PyEnum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"