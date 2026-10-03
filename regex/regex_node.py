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
    def __str__(
            self
        ) -> str:
        """
        Return the string representation of the regex node.

        Returns:
            str: The regex expression represented by this node.
        """
        pass

    @abstractmethod
    def __repr__(
            self
        ) -> str:
        """
        Return a developer-oriented representation of the regex node.

        Concrete node classes should include their type and recursively
        represent their child nodes where applicable.

        Returns:
            str: An unambiguous representation of the regex node.
        """
        pass

    def compare(
            self,
            other: 'RegexNode'
        ) -> int:
        """
        Compare the precedence of this node with another regex node.

        Args:
            other (RegexNode): The node to compare against.

        Raises:
            ValueError: If other is not a RegexNode instance.

        Returns:
            int: The difference in precedence between this node and other.
        """
        if not isinstance(other, RegexNode):
            raise ValueError("Can only compare with another RegexNode.")
        return self.precedence - other.precedence
