"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .regex_node import RegexNode


class BinaryNode(RegexNode):
    """
    Represents a regular-expression node that combines two child nodes.

    This is the base class for operators such as concatenation and union,
    where each node carries a left and a right operand.

    Attributes:
        left (RegexNode): The left-hand operand in the expression tree.
        right (RegexNode): The right-hand operand in the expression tree.
        precedence (int): The node precedence used when comparing operators.
    """

    left: RegexNode
    right: RegexNode
    precedence: int

    def __init__(
            self,
            left: RegexNode,
            right: RegexNode
        ) -> None:
        """
        Create a binary node for a pair of regex operands.

        Args:
            left (RegexNode): The left operand to attach to this node.
            right (RegexNode): The right operand to attach to this node.

        Raises:
            ValueError: If either child is None.
            TypeError: If either child is not a RegexNode instance.
        """
        if left is None or right is None:
            raise ValueError("Left and right children cannot be None")

        if not isinstance(left, RegexNode) or not isinstance(right, RegexNode):
            raise TypeError("Left and right must be instances of RegexNode")

        self.left = left
        self.right = right
