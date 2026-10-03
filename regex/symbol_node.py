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

    def __init__(
            self,
            symbol: RegexSymbol
        ) -> None:
        """
        Create a symbol node from a regex symbol.

        Args:
            symbol (RegexSymbol): The symbol this node should represent.
        """
        self.symbol = symbol

    def __str__(
            self
        ) -> str:
        """
        Return the textual representation of this symbol.

        Returns:
            str: The underlying regex symbol string.
        """
        return str(self.symbol)

    def __repr__(
            self
        ) -> str:
        """
        Return a developer-oriented representation of this symbol node.

        Returns:
            str: A representation containing the node type and symbol.
        """
        return f"SymbolNode(RegexSymbol.{self.symbol.name})"

    def __eq__(
            self,
            other: object
        ) -> bool:
        """
        Determine if this symbol node is equal to another symbol node.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True if the other object is a SymbolNode with the same symbol, False otherwise.
        """
        if not isinstance(other, SymbolNode):
            return False
        return self.symbol == other.symbol
