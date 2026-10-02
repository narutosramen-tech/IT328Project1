"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .state import State
from regex import RegularExpression


class Transition:
    """
    Represents a transition between two states in an automaton.

    Attributes:
        start (State): The start state of the transition.
        end (State): The end state of the transition.
        expression (RegularExpression): The RegularExpression required to take the transition.
    """
    start: State
    end: State
    expression: RegularExpression

    def __init__(
            self,
            start: State,
            end: State,
            expression: RegularExpression
        ) -> None:
        """
        Create a transition between two states.

        Args:
            start (State): The state where the transition begins.
            end (State): The state where the transition ends.
            expression (RegularExpression): The regular expression labeling the transition.
        """
        self.start = start
        self.end = end
        self.expression = expression

    def __eq__(
            self,
            other: object
        ) -> bool:
        """
        Determine whether this transition is equal to another transition.

        Two transitions are equal when they have the same starting state,
        ending state, and regular expression label.

        Args:
            other (object): The object to compare against

        Returns:
            bool: True for an equivalent Transition, False for a different one;
                otherwise NotImplemented for unsupported types.
        """
        if not isinstance(other, Transition):
            return NotImplemented

        return (
            self.start == other.start
            and self.end == other.end
            and self.expression == other.expression
        )

    def __str__(
            self
        ) -> str:
        """
        Return the transition in the assignment's required string format.

        Returns:
            str: The transition formatted as
                q<start>-<expression>->q<end>.
        """
        return f"q{self.start.name}-{self.expression}->q{self.end.name}"
