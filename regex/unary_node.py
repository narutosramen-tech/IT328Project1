from .regex_node import RegexNode

class UnaryNode(RegexNode):
    child: RegexNode
    precedence: int

    def __init__(self, child: RegexNode) -> None:
        if child is None:
            raise ValueError("Child node cannot be None")

        if not isinstance(child, RegexNode):
            raise TypeError("Child must be an instance of RegexNode")
        
        self.child = child