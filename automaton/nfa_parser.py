"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from regex import RegularExpression
from .nfa import NFA
from typing import Optional


class NFAParser:
    """
    Parse state and transition tokens into an NFA.

    Attributes:
        input_string (str): The definition with outer whitespace removed.
        nfa (Optional[NFA]): The current parsing result, or None before parsing.
    """

    input_string: str
    nfa: Optional[NFA]

    def __init__(
            self,
            string: str
        ) -> None:
        """
        Store an NFA definition for parsing.

        Args:
            string (str): Comma-separated state and transition definitions.
        """
        if not isinstance(string, str):
            raise TypeError("NFA input must be a string.")

        # Whitespace is insignificant in the machine-definition language.
        self.input_string = "".join(string.split())
        self.nfa = None

    def parse_state_token(
            self,
            token: str
        ) -> tuple[int, bool]:
        """
        Read a state name and its optional accepting-state marker.

        Args:
            token (str): A state token such as q0 or q2f.

        Raises:
            ValueError: If the token does not contain q followed by a
                nonnegative integer and an optional f suffix.

        Returns:
            tuple[int, bool]: The numeric state name and acceptance status.
        """
        token = token.strip()

        if not token.startswith("q"):
            raise ValueError(f"Invalid state token: {token}")

        is_accepting = token.endswith("f")

        number_text = token[1:-1] if is_accepting else token[1:]

        if not number_text.isdigit():
            raise ValueError(f"Invalid state token: {token}")

        return int(number_text), is_accepting

    def parse_transition_token(
            self,
            token: str
        ) -> tuple[int, int, RegularExpression]:
        """
        Read the endpoints and label of a transition.

        Args:
            token (str): A transition token such as q0-a->q1.

        Raises:
            ValueError: If the syntax or state names are invalid, either
                endpoint includes f, or the label is not a, b, or e.

        Returns:
            tuple[int, int, RegularExpression]: The starting state name,
                ending state name, and expression representing the label.
        """
        token = token.strip()

        if "->" not in token:
            raise ValueError(F"Invalid transition token: {token}")

        left_half, end_token = token.split("->", 1)

        if "-" not in left_half:
            raise ValueError(f"Invalid transition token: {token}")

        begin_token, label = left_half.split("-", 1)

        start_name, start_accept = self.parse_state_token(begin_token)
        end_name, end_accept = self.parse_state_token(end_token)

        if start_accept or end_accept:
            raise ValueError("Transition state references cannot include 'f'.")

        expression = None
        if label == "a":
            expression = RegularExpression.a()
        elif label == "b":
            expression = RegularExpression.b()
        elif label == "e":
            expression = RegularExpression.epsilon()
        else:
            raise ValueError(
                "Transition label must be 'a', 'b', or 'e' on an NFA."
            )

        return start_name, end_name, expression

    def parse(
            self
        ) -> NFA:
        """
        Build an NFA from the stored comma-separated definition.

        States must be declared before transitions that reference them.
        State q0 becomes the start state, and an f suffix marks acceptance.
        Each call creates a new NFA.

        Raises:
            ValueError: If a token is invalid, a state is duplicated, a
                transition references an undeclared state, or the resulting
                NFA fails structural validation.

        Returns:
            NFA: The parsed automaton.
        """
        if not self.input_string:
            raise ValueError("NFA input cannot be empty.")

        tokens = self.input_string.split(",")

        self.nfa = NFA()

        for token in tokens:
            if "->" not in token:
                name, accepting = self.parse_state_token(token)
                self.nfa.add_state(name, accepting)
                if name == 0:
                    self.nfa.set_start_state(name)
            else:
                start, end, expression = self.parse_transition_token(token)
                self.nfa.add_transition(start, end, expression)

        if not self.nfa.validate_complete():
            raise ValueError(f"The NFA has invalid states, transitions, or does not have a start state.")

        return self.nfa
