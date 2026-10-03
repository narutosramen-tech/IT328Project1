"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .gnfa import GNFA
from .nfa import NFA


class NFAToGNFAConverter:
    """
    Provide the public API for converting an NFA into a GNFA.

    The conversion itself is implemented by ``GNFA.from_nfa``. This wrapper
    gives callers a dedicated converter class without duplicating the GNFA
    construction logic.
    """

    @staticmethod
    def convert(
            nfa: NFA
        ) -> GNFA:
        """
        Convert an NFA into a normalized GNFA.

        Args:
            nfa (NFA): The valid NFA to convert.

        Raises:
            TypeError: If nfa is not an NFA instance.
            ValueError: If nfa is structurally incomplete.

        Returns:
            GNFA: A new GNFA containing copied states and normalized transitions.
        """
        if not isinstance(nfa, NFA):
            raise TypeError("NFA conversion requires an NFA instance.")

        return GNFA.from_nfa(nfa)

