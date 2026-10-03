"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .nfa import NFA
from .automaton import Automaton
from .transition import Transition
from .state import State
from regex import RegularExpression
from typing import List


class GNFA(Automaton):
    """
    An automaton whose transitions are labeled with regular expressions.

    Attributes:
        inner_states (list[State]): States copied from the original NFA.
        new_start_state (State): Start state added when copying an NFA.
        new_accept_state (State): Sole accepting state after copying an NFA.

    These attributes are initialized by _copy_from_nfa.
    """

    inner_states: list[State]
    new_start_state: State
    new_accept_state: State

    def __init__(
            self
        ) -> None:
        """
        Initialize the empty state and transition collections.
        """
        super().__init__()

    def validate_complete(
            self
        ) -> bool:
        """
        Check the structural requirements of this GNFA.

        A valid GNFA has a start state, exactly one accepting state, and
        transitions whose endpoints belong to the GNFA. When the GNFA was
        created from an NFA, every ordered pair of inner states must also
        have exactly one transition.

        Returns:
            bool: True when the GNFA satisfies these structural requirements.
        """
        if self.start_state is None or self.start_state not in self.states:
            return False

        if len(self.get_accepting_states()) != 1:
            return False

        if not all(
            transition.start in self.states
            and transition.end in self.states
            and isinstance(transition.expression, RegularExpression)
            for transition in self.transitions
        ):
            return False

        for state_start in getattr(self, "inner_states", []):
            for state_end in getattr(self, "inner_states", []):
                if len(self.get_transitions(state_start.name, state_end.name)) != 1:
                    return False

        return True

    def __str__(
            self
        ) -> str:
        """
        Return the GNFA in comma-separated definition format.

        States are listed before transitions. State and transition formatting
        is delegated to their respective ``__str__`` methods.

        Returns:
            str: The serialized GNFA definition with no spaces.
        """
        if (
            hasattr(self, "new_start_state")
            and hasattr(self, "new_accept_state")
            and hasattr(self, "inner_states")
        ):
            states = [
                self.new_start_state,
                *self.inner_states,
                self.new_accept_state,
            ]
        else:
            states = self.states

        definitions = [str(state) for state in states]
        definitions.extend(str(transition) for transition in self.transitions)
        return ",".join(definitions)

    def combine_transitions(
            self,
            transitions: List[Transition]
        ) -> None:
        """
        Replace parallel transitions with one union-labeled transition.

        Args:
            transitions (List[Transition]): A nonempty list of transitions
                in this automaton with matching start and end states.

        Raises:
            ValueError: If the supplied transitions have different endpoints
                or a supplied transition is not in this automaton.
        """
        if not isinstance(transitions, list):
            raise TypeError("Transitions must be supplied as a list.")

        if not transitions:
            raise ValueError("At least one transition is required.")

        if not all(isinstance(transition, Transition) for transition in transitions):
            raise TypeError("All items must be Transition instances.")

        if any(transition not in self.transitions for transition in transitions):
            raise ValueError("All transitions must belong to this GNFA.")

        # No combination is needed if there is only one supplied edge.
        if len(transitions) < 2:
            return

        start = transitions[0].start
        end = transitions[0].end

        for transition in transitions:
            if transition.start != start or transition.end != end:
                raise ValueError(
                    "All transitions being combined must have the same start and end state."
                )

        # Union preserves each alternative label between these endpoints.
        expression = transitions[0].expression

        for transition in transitions[1:]:
            expression = expression.union(transition.expression)

        # Replace the original edges with their combined expression.
        for transition in transitions:
            self.transitions.remove(transition)

        self.add_transition(
            start.name,
            end.name,
            expression
        )

    def _copy_from_nfa(
            self,
            nfa: NFA
        ) -> 'GNFA':
        """
        Populate an empty GNFA with NFA states and transitions.

        Add new boundary states, connect original accepting states to the
        new accepting state, and normalize transitions between inner states.

        Args:
            nfa (NFA): The source automaton to copy.

        Returns:
            GNFA: This instance after its states and transitions are populated.
        """
        if not nfa.validate_complete():
            raise ValueError("Cannot create a GNFA from an incomplete NFA.")

        # Create separate states so acceptance changes do not affect the NFA.
        for state in nfa.states:
            self.add_state(
                state.name,
                state.is_accepting
            )
        # Save the original states before adding the new boundary states.
        self.inner_states = list(self.states)

        for transition in nfa.transitions:
            self.add_transition(
                transition.start.name,
                transition.end.name,
                transition.expression
            )
        if nfa.start_state is not None:
            old_start_state = self.get_state(nfa.start_state.name)

        # Find two unused nonnegative state names for the boundary states.
        found_new_start = False
        found_new_accept = False
        i = 0
        while not found_new_accept:
            if self.get_state(i) is None:
                if not found_new_start:
                    self.new_start_state = self.add_state(i)
                    found_new_start = True
                else:
                    self.new_accept_state = self.add_state(i, True)
                    found_new_accept = True
            i += 1

        self.start_state = self.new_start_state

        # Connect the new start state to the copied original start state.
        if old_start_state is not None:
            self.add_transition(
                self.new_start_state.name,
                old_start_state.name,
                RegularExpression.epsilon()
        )

        # Transfer acceptance through epsilon edges to one accepting state.
        for state in self.states:
            if state != self.new_accept_state and state.is_accepting:
                self.add_transition(
                    state.name,
                    self.new_accept_state.name,
                    RegularExpression.epsilon()
                )
                state.is_accepting = False

        # Give each ordered pair of inner states exactly one edge, including
        # self-loops. Empty-set labels represent missing transitions.
        for state_start in self.inner_states:
            for state_end in self.inner_states:
                items = self.get_transitions(state_start.name, state_end.name)
                if len(items) > 1:
                    self.combine_transitions(items)
                elif len(items) == 0:
                    self.add_transition(state_start.name, state_end.name, RegularExpression.empty_set())

        if not self.validate_complete():
            raise ValueError("The converted GNFA is structurally incomplete.")

        return self

    @classmethod
    def from_nfa(
            cls,
            nfa: NFA
        ) -> 'GNFA':
        """
        Create an instance and populate it from the supplied NFA.

        Args:
            nfa (NFA): The source automaton to copy.

        Returns:
            GNFA: A new instance populated by _copy_from_nfa.
        """
        if not isinstance(nfa, NFA):
            raise TypeError("GNFA conversion requires an NFA instance.")

        gnfa = cls()
        gnfa._copy_from_nfa(nfa)
        return gnfa
