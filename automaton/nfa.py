from automaton import Automaton
from automaton.transition import Transition
from regex import RegularExpression

class NFA(Automaton):
    """A non-deterministic finite automaton (NFA) implementation.

    Attributes:
        states (list[State]): A list of all states in the NFA.
        transitions (list[Transition]): A list of all transitions in the NFA.
        start_state (State | None): The start state of the NFA.
    """
    def __init__(self) -> None:
        super().__init__()

    def add_transition(
            self, 
            start_name: int, 
            end_name: int, 
            expression: RegularExpression
        ) -> Transition:
        if (
            expression != RegularExpression.epsilon()
            and expression != RegularExpression.a()
            and expression != RegularExpression.b()
        ):
            raise ValueError(
                "NFA transitions can only be labeled with 'a', 'b', or epsilon."
            )
        
        return super().add_transition(start_name, end_name, expression)

    def validate_complete(self) -> bool:
        """Validates whether the NFA has a start state, whether the start state is valid, and whether the start state is missing from the list of states.

        Since all of these things can be directly manipulated (because Python has no private access classes), this validates that the NFA has not been broken.

        Returns:
            bool: True if the NFA is complete, False otherwise.
        """
        if self.start_state is None or self.start_state not in self.states:
            return False

        if self.start_state.name != 0:
            return False

        return all(
            transition.start in self.states
            and transition.end in self.states
            for transition in self.transitions
        )
