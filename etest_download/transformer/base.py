from abc import ABC, abstractmethod
from typing import Any


class BaseTransformer(ABC):
    @classmethod
    @abstractmethod
    def transform(cls, data: Any) -> Any:
        pass
