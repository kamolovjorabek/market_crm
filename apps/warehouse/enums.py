from enum import Enum


class RequestStatus(Enum):
    new = 'new'
    accepted = 'accepted'  #Qabul qilingan
    rejected = 'rejected'  #Rad etilgan
    confirmed = 'confirmed'  #Tasdiqlangan

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]
