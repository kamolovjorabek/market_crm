from enum import Enum


class UserRole(Enum):
    director = "director"
    warehouse = "warehouse"
    shop = "shop"

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]
