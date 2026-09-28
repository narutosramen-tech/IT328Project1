"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .regex_symbol import RegexSymbol
from .regex_node import RegexNode


class SymbolNode(RegexNode):
    """
    Represents a single regex symbol such as 'a', 'b', epsilon, or empty set.

    Attributes:
        symbol (RegexSymbol): The symbol value represented by this node.
        precedence (int): Symbol precedence value, set to 4.
    """

    symbol: RegexSymbol
    precedence: int = 4

    def __init__(self, symbol: RegexSymbol) -> None:
        """
        Create a symbol node from a regex symbol.

        @param symbol: The symbol this node should represent.
        """
        self.symbol = symbol

    def __str__(self) -> str:
        """
        Return the textual representation of this symbol.

        @return: The underlying regex symbol string.
        """
        return str(self.symbol)