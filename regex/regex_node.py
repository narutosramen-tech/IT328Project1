"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from abc import ABC, abstractmethod
from .stringable import Stringable
from .precedence_aware import PrecedenceAware


class RegexNode(Stringable, PrecedenceAware, ABC):
    """
    Abstract base class for all regex expression nodes.

    Every concrete regex node must be string-convertible and participate in
    precedence-based rendering rules.

    Attributes:
        precedence (int): The precedence level of the node within a regex tree.
    """

    precedence: int

    @abstractmethod
    def __str__(self) -> str:
        """
        Return the string representation of the regex node.

        @return: The regex expression represented by this node.
        """
        pass

    def compare(self, other: 'RegexNode') -> int:
        """
        Compare the precedence of this node with another regex node.

        @param other: The node to compare against.
        @return: The difference in precedence between this node and other.
        @raises ValueError: If other is not a RegexNode instance.
        """
        if not isinstance(other, RegexNode):
            raise ValueError("Can only compare with another RegexNode.")
        return self.precedence - other.precedence
