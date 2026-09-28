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

    def __init__(self, left: RegexNode, right: RegexNode) -> None:
        """
        Create a union node between two regex expressions.

        @param left: The left-hand branch of the union.
        @param right: The right-hand branch of the union.
        """
        super().__init__(left, right)

    def __str__(self) -> str:
        """
        Return the regex string for a union expression.

        @return: The union formatted as left U right.
        """
        return f"{self.left}U{self.right}"

    def __eq__(self, other: object) -> bool:
        """
        Determine if this union node is equal to another union node.

        @param other: The object to compare against.
        @return: True if the other object is a UnionNode containing the same two child expressions, regardless of order.
        """
        if not isinstance(other, UnionNode):
            return False
        return (
            (self.left == other.left and self.right == other.right)
            or (self.left == other.right and self.right == other.left)
        )
