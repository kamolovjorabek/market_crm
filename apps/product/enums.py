from enum import Enum


class Measure(Enum):
    kg = 'kg'
    liter = 'liter'
    piece = 'piece'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]


class WarehouseStatus(Enum):
    sent = 'sent'
    confirmed = 'confirmed'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]
