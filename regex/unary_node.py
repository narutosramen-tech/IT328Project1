"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .regex_node import RegexNode


class UnaryNode(RegexNode):
    """
    Base class for regex operations that take exactly one child node.

    This includes operators such as star and any future unary constructs that
    need to validate a single operand before forming a regex expression.

    Attributes:
        child (RegexNode): The operand on which the unary operation acts.
        precedence (int): The relative precedence assigned to the operation.
    """

    child: RegexNode
    precedence: int

    def __init__(self, child: RegexNode) -> None:
        """
        Create a unary regex node around a single child expression.

        @param child: The regex node to wrap.
        @raises ValueError: If the child is None.
        @raises TypeError: If the child is not a RegexNode instance.
        """
        if child is None:
            raise ValueError("Child node cannot be None")

        if not isinstance(child, RegexNode):
            raise TypeError("Child must be an instance of RegexNode")

        self.child = child