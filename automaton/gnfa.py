from .nfa import NFA
from .automaton import Automaton
from .transition import Transition
from .state import State
from regex import RegularExpression
from typing import List

class GNFA(Automaton):
    inner_states: list[State]
    new_start_state: State
    new_accept_state: State

    def __init__(self) -> None:
        super().__init__()

    def combine_transitions(self, transitions: List[Transition]) -> None:
        if len(self.transitions) < 2:
            return

        start = transitions[0].start
        end = transitions[0].end

        for transition in transitions:
            if transition.start != start or transition.end != end:
                raise ValueError(
                    "All transitions being combined must have the same start and end state."
                )

        expression = transitions[0].expression

        for transition in transitions[1:]:
            expression = expression.union(transition.expression)

        for transition in transitions:
            self.transitions.remove(transition)

        self.add_transition(
            start.name,
            end.name,
            expression
        )

    def _copy_from_nfa(self, nfa: NFA) -> 'GNFA':
        for state in nfa.states:
            self.add_state(
                state.name,
                state.is_accepting
            )
        self.inner_states = list(self.states)

        for transition in nfa.transitions:
            self.add_transition(
                transition.start.name,
                transition.end.name,
                transition.expression
            )

        if nfa.start_state is not None:
            self.start_state = self.get_state(nfa.start_state.name)

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

        for state in self.states:
            if state != self.new_accept_state and state.is_accepting:
                self.add_transition(
                    state.name,
                    self.new_accept_state.name,
                    RegularExpression.epsilon()
                )
                state.is_accepting = False

        for state_start in self.inner_states:
            for state_end in self.inner_states:
                items = self.get_transitions(state_start.name, state_end.name)
                if len(items) > 1:
                    self.combine_transitions(items)
                elif len(items) == 0:
                    self.add_transition(state_start.name, state_end.name, RegularExpression.empty_set())

        return self

    @classmethod
    def from_nfa(cls, nfa: NFA) -> 'GNFA':
        gnfa = cls()
        gnfa._copy_from_nfa(nfa)
        return gnfa
    