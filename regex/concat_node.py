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

    def __init__(self, left: RegexNode, right: RegexNode) -> None:
        """
        Create a concatenation node around two regex fragments.

        @param left: The left expression in the concatenation.
        @param right: The right expression in the concatenation.
        """
        super().__init__(left, right)

    def __str__(self) -> str:
        """
        Convert the concatenation into a readable regular-expression string.

        Parentheses are added around child expressions only when their
        precedence is lower than the current node.

        @return: The concatenated regex string representation.
        """
        left = str(self.left)
        right = str(self.right)

        if self.compare(self.left) > 0:
            left = f"({left})"

        if self.compare(self.right) > 0:
            right = f"({right})"

        return f"{left}{right}"