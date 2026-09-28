from .binary_node import BinaryNode
from .regex_node import RegexNode

class ConcatNode(BinaryNode):
    precedence: int = 2

    def __init__(self, left: RegexNode, right: RegexNode) -> None:
        super().__init__(left, right)

    def __str__(self) -> str:
        left = str(self.left)
        right = str(self.right)

        if self.compare(self.left) > 0:
            left = f"({left})"

        if self.compare(self.right) > 0:
            right = f"({right})"

        return f"{left}{right}"