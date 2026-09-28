"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .unary_node import UnaryNode


class StarNode(UnaryNode):
    """
    Represents the Kleene star operation applied to a single regex node.

    The star operation gives a node the highest precedence among the
    currently supported operators and may wrap child expressions when needed.

    Attributes:
        precedence (int): Star precedence value set to 3.
    """

    precedence: int = 3

    def __init__(self, child: UnaryNode) -> None:
        """
        Create a star node around a unary regex operand.

        @param child: The regex expression to apply the star operator to.
        """
        super().__init__(child)

    def __str__(self) -> str:
        """
        Return the regex string for the star operation.

        Parentheses are added to child expressions with lower precedence.

        @return: The star-formatted regex string.
        """
        child_str = str(self.child)

        if self.compare(self.child) > 0:
            child_str = f"({child_str})"

        return f"{child_str}*"