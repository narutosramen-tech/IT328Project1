"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""


class PrecedenceAware:
    """
    Provides a common comparison contract for regex nodes that have a precedence.

    Subclasses use this interface to decide whether a child expression must
    be wrapped in parentheses during string formatting.
    """

    def compare(self, other: 'PrecedenceAware') -> int:
        """
        Compare this object against another precedence-aware node.

        @param other: The other node to compare against.
        @return: A relative precedence difference.
        @raises NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement compare method.")