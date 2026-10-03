"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .binary_node import BinaryNode
from .regex_node import RegexNode


class UnionNode(BinaryNode):
    """
    Represents a union between two regular-expression operands.

    The union operator is the lowest-precedence binary operation in the
    current implementation and is rendered with an uppercase 'U' separator.

    Attributes:
        precedence (int): Union precedence value, set to 1.
    """

    precedence: int = 1

    def __init__(
            self,
            left: RegexNode,
            right: RegexNode
        ) -> None:
        """
        Create a union node between two regex expressions.

        Args:
            left (RegexNode): The left-hand branch of the union.
            right (RegexNode): The right-hand branch of the union.

        Raises:
            ValueError: If either child is None.
            TypeError: If either child is not a RegexNode instance.
        """
        super().__init__(left, right)

    def __str__(
            self
        ) -> str:
        """
        Return the regex string for a union expression.

        Returns:
            str: The union formatted as left U right.
        """
        return f"{self.left}U{self.right}"

    def __repr__(
            self
        ) -> str:
        """
        Return a developer-oriented representation of this union node.

        Returns:
            str: A recursive representation of both union operands.
        """
        return f"UnionNode({repr(self.left)}, {repr(self.right)})"

    def __eq__(
            self,
            other: object
        ) -> bool:
        """
        Determine if this union node is equal to another union node.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True if the other object is a UnionNode containing the same two child expressions, regardless of order.
        """
        if not isinstance(other, UnionNode):
            return False
        return (
            (self.left == other.left and self.right == other.right)
            or (self.left == other.right and self.right == other.left)
        )
