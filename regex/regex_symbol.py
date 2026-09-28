"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from enum import Enum


class RegexSymbol(Enum):
    """
    Enumeration of the literal symbols used in this regex implementation.

    Each member corresponds to a textual symbol that can appear within a
    regular expression or transition model.

    Attributes:
        A (str): The lowercase symbol 'a'.
        B (str): The lowercase symbol 'b'.
        EPSILON (str): The epsilon symbol 'e'.
        EMPTY_SET (str): The empty-set symbol 'es'.
    """

    # The symbol for the literal 'a'.
    A = "a"
    # The symbol for the literal 'b'.
    B = "b"
    # The epsilon symbol used to represent empty transition behavior.
    EPSILON = "e"
    # The symbol used to represent the empty set.
    EMPTY_SET = "es"

    def __str__(self):
        """
        Return the string value stored by the enum member.

        @return: The raw symbol text used by the regex representation.
        """
        return self.value