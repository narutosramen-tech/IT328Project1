"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .state import State
from .transition import Transition
from regex import RegularExpression
from typing import Optional


class Automaton:
    """An implementation neutral automaton that can be either a NFA or a GNFA.

    Attributes:
        states (list[State]): A list of all states in the automaton.
        transitions (list[Transition]): A list of all transitions in the automaton.
        start_state (State | None): The start state of the automaton.
    """
    states: list[State]
    transitions: list[Transition]
    start_state: Optional[State]

    def __init__(self) -> None:
        self.states = []
        self.transitions = []
        self.start_state = None

    def get_state(self, name: int) -> Optional[State]:
        return next((s for s in self.states if s.name == name), None)

    def get_transitions(self, start_name: int, end_name: int) -> list[Transition]:
        return [t for t in self.transitions if t.start.name == start_name and t.end.name == end_name]

#    def get_specific_transitions(self, start_name: int, end_name: int) -> list[Transition]:
#        start_state = self.get_state(start_name)
#        end_state = self.get_state(end_name)
#
#        results = []
#        if start_state is None or end_state is None:
#            return results
#        
#        for t in self.transitions:
#            if t.start == start_state and t.end == end_state:
#                results.append(t)
#
#        return results

    def add_state(self, name: int, is_accepting: bool = False) -> State:
        state = State(name, is_accepting)

        if state not in self.states:
            self.states.append(state)
        else:
            raise ValueError(f"State with name {name} already exists.")
        return state

    def set_start_state(self, name: int) -> None:
        state = self.get_state(name)

        if state is None:
            raise ValueError(f"State with name {name} does not exist.")
        
        self.start_state = state

    def remove_state(self, name: int) -> None:
        state = self.get_state(name)

        if state is None:
            raise ValueError(f"State with name {name} does not exist.")
        
        if state in self.states:
            self.states.remove(state)
            self.transitions = [t for t in self.transitions if t.start != state and t.end != state]

            if self.start_state == state:
                self.start_state = None

    def add_transition(self, start_name: int, end_name: int, expression: RegularExpression) -> Transition:
        start_state = self.get_state(start_name)
        end_state = self.get_state(end_name)

        if start_state is None or end_state is None:
            raise ValueError("Start or end state does not exist.")

        transition = Transition(start_state, end_state, expression)
        self.transitions.append(transition)
        return transition

    def remove_transition(self, start_name: int, end_name: int) -> None:
        transitions = self.get_transitions(start_name, end_name)

        if not transitions:
            raise ValueError("No transitions found for the given start and end states.")
        
        for transition in transitions:
            if transition in self.transitions:
                self.transitions.remove(transition)

    def get_accepting_states(self) -> list[State]:
        return [s for s in self.states if s.is_accepting]

    def get_incoming_transitions(self, state_name: int) -> list[Transition]:
        state = self.get_state(state_name)

        if state is None:
            raise ValueError("State does not exist.")
        
        return [t for t in self.transitions if t.end == state and t.start != state]

    def get_outgoing_transitions(self, state_name: int) -> list[Transition]:
        state = self.get_state(state_name)

        if state is None:
            raise ValueError("State does not exist.")
        
        return [t for t in self.transitions if t.start == state and t.end != state]

    def get_self_loops(self, state_name: int) -> list[Transition]:
        state = self.get_state(state_name)

        if state is None:
            raise ValueError("State does not exist.")
        
        return [t for t in self.transitions if t.start == state and t.end == state]
