from regex import RegularExpression
from .nfa import NFA
from typing import Optional

class NFAParser:
    input_string: str
    nfa: Optional[NFA]

    def __init__(self, string: str) -> None:
        self.input_string = string.strip()
        self.nfa = None

    def parse_state_token(self, token: str) -> tuple[int, bool]:
        token = token.strip()
        
        if not token.startswith("q"):
            raise ValueError(f"Invalid state token: {token}")

        is_accepting = token.endswith("f")

        number_text = token[1:-1] if is_accepting else token[1:]

        if not number_text.isdigit():
            raise ValueError(f"Invalid state token: {token}")

        return int(number_text), is_accepting

    def parse_transition_token(self, token: str) -> tuple[int, int, RegularExpression]:
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

    def parse(self) -> NFA:
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
