from .binary_node import BinaryNode
from .regex_node import RegexNode

class UnionNode(BinaryNode):
    precedence: int = 1

    def __init__(self, left: RegexNode, right: RegexNode) -> None:
        super().__init__(left, right)

    def __str__(self) -> str:
        return f"({self.left}U{self.right})"