"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from automaton import Automaton
from automaton.transition import Transition
from regex import RegularExpression


class NFA(Automaton):
    """
    A non-deterministic finite automaton (NFA) implementation.

    Attributes:
        states (list[State]): A list of all states in the NFA.
        transitions (list[Transition]): A list of all transitions in the NFA.
        start_state (State | None): The start state of the NFA.
    """
    def __init__(
            self
        ) -> None:
        """
        Create an empty NFA with no states, transitions, or start state.
        """
        super().__init__()

    def __str__(
            self
        ) -> str:
        """
        Return the NFA in comma-separated definition format.

        States are listed before transitions. State and transition formatting
        is delegated to their respective ``__str__`` methods.

        Returns:
            str: The serialized NFA definition with no spaces.
        """
        definitions = [str(state) for state in self.states]
        definitions.extend(str(transition) for transition in self.transitions)
        return ",".join(definitions)

    def add_transition(
            self,
            start_name: int,
            end_name: int,
            expression: RegularExpression
        ) -> Transition:
        """
        Add an a, b, or epsilon transition between existing states.

        Args:
            start_name (int): The numeric name of the starting state.
            end_name (int): The numeric name of the ending state.
            expression (RegularExpression): The symbol labeling the transition.

        Raises:
            ValueError: If the label is not a, b, or epsilon, or either state
                does not exist.

        Returns:
            Transition: The newly created transition.
        """
        if (
            expression != RegularExpression.epsilon()
            and expression != RegularExpression.a()
            and expression != RegularExpression.b()
        ):
            raise ValueError(
                "NFA transitions can only be labeled with 'a', 'b', or epsilon."
            )

        return super().add_transition(start_name, end_name, expression)

    def validate_complete(
            self
        ) -> bool:
        """
        Check the start state and transition endpoints.

        The start state must belong to the NFA and have the numeric name 0.
        Every transition endpoint must also belong to the NFA.

        Returns:
            bool: True if these structural checks pass, False otherwise.
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
