from .unary_node import UnaryNode

class StarNode(UnaryNode):
    precedence: int = 3

    def __init__(self, child: UnaryNode) -> None:
        super().__init__(child)

    def __str__(self) -> str:
        child_str = str(self.child)

        if self.compare(self.child) > 0:
            child_str = f"({child_str})"
            
        return f"{child_str}*"