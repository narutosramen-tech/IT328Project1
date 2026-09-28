from abc import ABC, abstractmethod
from .stringable import Stringable
from .precedence_aware import PrecedenceAware

class RegexNode(Stringable, PrecedenceAware, ABC):
    precedence: int

    @abstractmethod
    def __str__(self) -> str:
        pass

    def compare(self, other: 'RegexNode') -> int:
        if not isinstance(other, RegexNode):
            raise ValueError("Can only compare with another RegexNode.")
        return self.precedence - other.precedence