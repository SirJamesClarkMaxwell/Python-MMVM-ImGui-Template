import attr
from abc import ABC
from models.model import Model
from data.data import Data


@attr.s(auto_attribs=True)
class ViewModel(ABC):
    model: Model
    data: Data
