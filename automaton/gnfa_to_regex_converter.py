"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .gnfa import GNFA
from regex import RegularExpression


class GNFAToRegexConverter:
    """
    Convert a normalized GNFA into an equivalent regular expression.

    State elimination is performed without mutating the supplied GNFA.
    """

    @staticmethod
    def convert(
            gnfa: GNFA
        ) -> RegularExpression:
        """
        Eliminate all inner states from a GNFA.

        For each eliminated state k, update every remaining pair i, j using:

        ``Rij = Rij U Rik(Rkk)*Rkj``

        Args:
            gnfa (GNFA): The normalized GNFA to convert.

        Raises:
            TypeError: If gnfa is not a GNFA instance.
            ValueError: If gnfa is structurally incomplete or does not have
                distinct boundary states.

        Returns:
            RegularExpression: The expression labeling the final start-to-
                accepting path. This is `e` when the GNFA accepts only the
                empty string and `es` when no accepting path exists; the
                converter never returns None.
        """
        if not isinstance(gnfa, GNFA):
            raise TypeError("Regex conversion requires a GNFA instance.")

        if not gnfa.validate_complete():
            raise ValueError("Cannot convert an incomplete GNFA.")

        if not hasattr(gnfa, "new_start_state") or not hasattr(
                gnfa,
                "new_accept_state"
            ):
            raise ValueError("GNFA boundary states are not defined.")

        start_state = gnfa.new_start_state
        accept_state = gnfa.new_accept_state

        if start_state == accept_state:
            raise ValueError("GNFA start and accepting states must differ.")

        active_states = list(gnfa.states)
        labels: dict[tuple[int, int], RegularExpression] = {}

        for start in active_states:
            for end in active_states:
                label = RegularExpression.empty_set()

                for transition in gnfa.get_transitions(start.name, end.name):
                    label = label.union(transition.expression)

                labels[(start.name, end.name)] = label

        eliminated_states = [
            state for state in active_states
            if state != start_state and state != accept_state
        ]

        for eliminated in eliminated_states:
            loop = labels[(eliminated.name, eliminated.name)].kleene_star()
            remaining_states = [
                state for state in active_states
                if state != eliminated
            ]

            for start in remaining_states:
                for end in remaining_states:
                    through_eliminated = (
                        labels[(start.name, eliminated.name)]
                        .concatenate(loop)
                        .concatenate(labels[(eliminated.name, end.name)])
                    )

                    labels[(start.name, end.name)] = (
                        labels[(start.name, end.name)]
                        .union(through_eliminated)
                    )

            active_states.remove(eliminated)

        return labels[(start_state.name, accept_state.name)]
