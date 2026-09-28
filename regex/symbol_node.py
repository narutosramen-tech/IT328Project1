from .regex_symbol import RegexSymbol
from .regex_node import RegexNode

class SymbolNode(RegexNode):
    symbol: RegexSymbol
    precedence: int = 4

    def __init__(self, symbol: RegexSymbol) -> None:
        self.symbol = symbol

    def __str__(self) -> str:
        return str(self.symbol)