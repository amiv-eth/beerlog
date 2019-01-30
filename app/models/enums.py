# app/models/enums.py

from enum import Enum


class BaseEnum(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class BeverageTypeEnum(BaseEnum):
    BEER = 'beer'
    COFFEE = 'coffee'


class OrganisationEnum(BaseEnum):
    AMIV = 'amiv'
    VIS = 'vis'
    VMP = 'vmp'
