"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .gnfa import GNFA
from regex import RegularExpression


class GNFAParser:
    """
    Parse normalized GNFA definitions and regular-expression labels.

    The first declared state is interpreted as the GNFA start state and the
    last declared state must be the sole accepting state. All states must be
    declared before transitions.
    """

    input_string: str

    def __init__(
            self,
            string: str
        ) -> None:
        """
        Store a GNFA definition for parsing.

        Args:
            string (str): Comma-separated state and transition definitions.

        Raises:
            TypeError: If string is not a string.
        """
        if not isinstance(string, str):
            raise TypeError("GNFA input must be a string.")

        # Whitespace is insignificant in the machine-definition language.
        self.input_string = "".join(string.split())

    def parse_state_token(
            self,
            token: str
        ) -> tuple[int, bool]:
        """
        Parse a state token such as q3 or q7f.

        Args:
            token (str): The state token to parse.

        Raises:
            ValueError: If token is not a valid state name.

        Returns:
            tuple[int, bool]: The numeric state name and acceptance status.
        """
        if not token.startswith("q"):
            raise ValueError(f"Invalid state token: {token}")

        accepting = token.endswith("f")
        number_text = token[1:-1] if accepting else token[1:]

        if not number_text.isdigit():
            raise ValueError(f"Invalid state token: {token}")

        return int(number_text), accepting

    def parse_transition_endpoint(
            self,
            token: str
        ) -> int:
        """
        Parse a non-accepting transition endpoint.

        Args:
            token (str): An endpoint such as q2.

        Raises:
            ValueError: If token is invalid or includes an accepting marker.

        Returns:
            int: The numeric state name.
        """
        name, accepting = self.parse_state_token(token)

        if accepting:
            raise ValueError("Transition endpoints cannot include 'f'.")

        return name

    def parse_regular_expression(
            self,
            expression: str
        ) -> RegularExpression:
        """
        Parse a regular-expression label.

        Supported syntax includes a, b, e, es, union with U, implicit
        concatenation, Kleene star, and parentheses.

        Args:
            expression (str): The expression to parse.

        Raises:
            ValueError: If expression has invalid syntax.

        Returns:
            RegularExpression: The parsed expression tree.
        """
        if not expression:
            raise ValueError("Transition expression cannot be empty.")

        position = 0

        def peek() -> str:
            if position >= len(expression):
                return ""
            return expression[position]

        def parse_union() -> RegularExpression:
            nonlocal position
            result = parse_concatenation()

            while peek() == "U":
                position += 1
                result = result.union(parse_concatenation())

            return result

        def parse_concatenation() -> RegularExpression:
            nonlocal position
            if peek() not in {"a", "b", "e", "("}:
                raise ValueError("Expected a regular-expression operand.")

            result = parse_repetition()

            while peek() in {"a", "b", "e", "("}:
                result = result.concatenate(parse_repetition())

            return result

        def parse_repetition() -> RegularExpression:
            nonlocal position
            result = parse_atom()

            if peek() == "*":
                position += 1
                result = result.kleene_star()

            return result

        def parse_atom() -> RegularExpression:
            nonlocal position
            symbol = peek()

            if expression[position:position + 2] == "es":
                position += 2
                return RegularExpression.empty_set()

            if symbol == "a":
                position += 1
                return RegularExpression.a()

            if symbol == "b":
                position += 1
                return RegularExpression.b()

            if symbol == "e":
                position += 1
                return RegularExpression.epsilon()

            if symbol == "(":
                position += 1
                result = parse_union()

                if peek() != ")":
                    raise ValueError("Missing closing parenthesis.")

                position += 1
                return result

            raise ValueError(f"Invalid regular-expression symbol: {symbol}")

        result = parse_union()

        if position != len(expression):
            raise ValueError(
                f"Unexpected regular-expression symbol: {expression[position]}"
            )

        return result

    def parse_transition_token(
            self,
            token: str,
            gnfa: GNFA
        ) -> None:
        """
        Parse and add one GNFA transition.

        Args:
            token (str): A transition such as q0-(aUb)->q1.
            gnfa (GNFA): The GNFA being populated.

        Raises:
            ValueError: If the transition is malformed or references an
                undeclared state.
        """
        if token.count("->") != 1:
            raise ValueError(f"Invalid transition token: {token}")

        left, end_token = token.split("->")

        if left.count("-") != 1:
            raise ValueError(f"Invalid transition token: {token}")

        start_token, expression_text = left.split("-")
        start_name = self.parse_transition_endpoint(start_token)
        end_name = self.parse_transition_endpoint(end_token)

        if gnfa.get_state(start_name) is None or gnfa.get_state(end_name) is None:
            raise ValueError("Transition references an undeclared state.")

        if gnfa.get_transitions(start_name, end_name):
            raise ValueError("GNFA cannot contain duplicate state-pair transitions.")

        gnfa.add_transition(
            start_name,
            end_name,
            self.parse_regular_expression(expression_text)
        )

    def parse(
            self
        ) -> GNFA:
        """
        Build a GNFA from the stored definition string.

        The first declared state becomes the start state. The final declared
        state must be the sole accepting state. States must precede all
        transitions.

        Raises:
            ValueError: If the definition is malformed or not normalized.

        Returns:
            GNFA: The parsed and validated GNFA.
        """
        if not self.input_string:
            raise ValueError("GNFA input cannot be empty.")

        tokens = self.input_string.split(",")
        state_tokens: list[str] = []
        transition_tokens: list[str] = []
        found_transition = False

        for token in tokens:
            if not token:
                raise ValueError("GNFA input contains an empty token.")

            if "->" in token:
                found_transition = True
                transition_tokens.append(token)
            elif found_transition:
                raise ValueError("GNFA states must precede transitions.")
            else:
                state_tokens.append(token)

        if len(state_tokens) < 2:
            raise ValueError("A GNFA requires a start and accepting state.")

        parsed_states = [self.parse_state_token(token) for token in state_tokens]

        if parsed_states[0][1]:
            raise ValueError("The first GNFA state cannot be accepting.")

        if not parsed_states[-1][1]:
            raise ValueError("The final GNFA state must be accepting.")

        if any(accepting for _, accepting in parsed_states[1:-1]):
            raise ValueError("Only the final GNFA state may be accepting.")

        gnfa = GNFA()

        for name, accepting in parsed_states:
            gnfa.add_state(name, accepting)

        gnfa.new_start_state = gnfa.states[0]
        gnfa.inner_states = list(gnfa.states[1:-1])
        gnfa.new_accept_state = gnfa.states[-1]
        gnfa.start_state = gnfa.new_start_state

        for token in transition_tokens:
            self.parse_transition_token(token, gnfa)

        if not gnfa.validate_complete():
            raise ValueError("The GNFA definition is structurally incomplete.")

        return gnfa
