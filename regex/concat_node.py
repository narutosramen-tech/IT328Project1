"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .binary_node import BinaryNode
from .regex_node import RegexNode


class ConcatNode(BinaryNode):
    """
    Represents concatenation of two regular expressions.

    The precedence of concatenation is higher than union and lower than
    star, which allows the class to parenthesize operands when needed.

    Attributes:
        precedence (int): Concatenation precedence value, set to 2.
    """

    precedence: int = 2

    def __init__(
            self,
            left: RegexNode,
            right: RegexNode
        ) -> None:
        """
        Create a concatenation node around two regex fragments.

        Args:
            left (RegexNode): The left expression in the concatenation.
            right (RegexNode): The right expression in the concatenation.

        Raises:
            ValueError: If either child is None.
            TypeError: If either child is not a RegexNode instance.
        """
        super().__init__(left, right)

    def __str__(
            self
        ) -> str:
        """
        Convert the concatenation into a readable regular-expression string.

        Parentheses are added around child expressions only when their
        precedence is lower than the current node.

        Returns:
            str: The concatenated regex string representation.
        """
        left = str(self.left)
        right = str(self.right)

        if self.compare(self.left) > 0:
            left = f"({left})"

        if self.compare(self.right) > 0:
            right = f"({right})"

        return f"{left}{right}"

    def __repr__(
            self
        ) -> str:
        """
        Return a developer-oriented representation of this concatenation node.

        Returns:
            str: A recursive representation of both concatenation operands.
        """
        return f"ConcatNode({repr(self.left)}, {repr(self.right)})"

    def __eq__(
            self,
            other: object
        ) -> bool:
        """
        Determine if this concatenation node is equal to another concatenation node.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True if the other object is a ConcatNode with the same left and right children, False otherwise.
        """
        if not isinstance(other, ConcatNode):
            return False
        return self.left == other.left and self.right == other.right
