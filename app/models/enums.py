# app/models/enums.py

from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class ProductEnum(BaseEnum):
    BEER = 'beer'
    COFFEE = 'coffee'

    @staticmethod
    def from_str(label):
        if label == 'beer':
            return ProductEnum.BEER
        if label == 'coffee':
            return ProductEnum.COFFEE
        return None

    @classmethod
    def choices(cls):
        return [(choice, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return item if (item == None or type(item) == ProductEnum) else ProductEnum[item]

class OrganisationEnum(BaseEnum):
    AMIV = 'amiv'
    VIS = 'vis'
    VMP = 'vmp'

    @staticmethod
    def from_str(label):
        if label == 'amiv':
            return OrganisationEnum.AMIV
        if label == 'vis':
            return OrganisationEnum.VIS
        if label == 'vmp':
            return OrganisationEnum.VMP
        return None

    @classmethod
    def choices(cls):
        return [(choice, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return item if (item == None or type(item) == OrganisationEnum) else OrganisationEnum[item]
