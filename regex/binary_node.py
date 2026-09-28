from .regex_node import RegexNode

class BinaryNode(RegexNode):
    left: RegexNode
    right: RegexNode
    precedence: int

    def __init__(self, left: RegexNode, right: RegexNode) -> None:
        if left is None or right is None:
            raise ValueError("Left and right children cannot be None")

        if not isinstance(left, RegexNode) or not isinstance(right, RegexNode):
            raise TypeError("Left and right must be instances of RegexNode")
        
        self.left = left
        self.right = right