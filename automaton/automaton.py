"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from abc import ABC, abstractmethod
from .state import State
from .transition import Transition
from regex import RegularExpression
from typing import Optional


class Automaton(ABC):
    """
    An implementation neutral automaton that can be either an NFA or a GNFA.

    Attributes:
        states (list[State]): A list of all states in the automaton.
        transitions (list[Transition]): A list of all transitions in the automaton.
        start_state (State | None): The start state of the automaton.
    """
    states: list[State]
    transitions: list[Transition]
    start_state: Optional[State]

    def __init__(
            self
        ) -> None:
        """
        Create an empty automaton with no states, transitions, or start state.
        """
        self.states = []
        self.transitions = []
        self.start_state = None

    def get_state(
            self,
            name: int
        ) -> Optional[State]:
        """
        Find a state by its numeric name.

        Args:
            name (int): The numeric name of the state to find.

        Returns:
            Optional[State]: The matching state, or None if no state with the specified name exists.
        """
        return next((s for s in self.states if s.name == name), None)

    def get_transitions(
            self,
            start_name: int,
            end_name: int
        ) -> list[Transition]:
        """
        Find all transitions between two states.

        Args:
            start_name (int): The numeric name of the starting state.
            end_name (int): The numeric name of the ending state.

        Returns:
            list[Transition]: A list of transitions from the starting state to the
                ending state. The list is empty if no transitions exist.
        """
        return [t for t in self.transitions if t.start.name == start_name and t.end.name == end_name]

    def add_state(
            self,
            name: int,
            is_accepting: bool = False
        ) -> State:
        """
        Add a new state to the automaton.

        Args:
            name (int): The numeric name of the new state.
            is_accepting (bool, optional): Whether the new state is
                an accepting state. Defaults to False.

        Raises:
            ValueError: If a state with the specified name already exists.

        Returns:
            State: The newly created state.
        """
        if not isinstance(name, int) or isinstance(name, bool):
            raise TypeError("State name must be an integer.")

        if not isinstance(is_accepting, bool):
            raise TypeError("is_accepting must be a boolean.")

        state = State(name, is_accepting)

        if state not in self.states:
            self.states.append(state)
        else:
            raise ValueError(f"State with name {name} already exists.")
        return state

    def set_start_state(
            self,
            name: int
        ) -> None:
        """
        Set an existing state as the start state.

        Args:
            name (int): The numeric name of the state to make the start state.

        Raises:
            ValueError: If no state with the specified name exists.
        """
        if not isinstance(name, int) or isinstance(name, bool):
            raise TypeError("State name must be an integer.")

        state = self.get_state(name)

        if state is None:
            raise ValueError(f"State with name {name} does not exist.")

        self.start_state = state

    def remove_state(
            self,
            name: int
        ) -> None:
        """
        Remove a state and all transitions connected to it.

        If the removed state is the current start state, the automaton's start
        state is reset to None.

        Args:
            name (int): The numeric name of the state to remove.

        Raises:
            ValueError: If no state with the specified name exists.
        """
        state = self.get_state(name)

        if state is None:
            raise ValueError(f"State with name {name} does not exist.")

        if state in self.states:
            self.states.remove(state)
            self.transitions = [t for t in self.transitions if t.start != state and t.end != state]

            if self.start_state == state:
                self.start_state = None

    def add_transition(
            self,
            start_name: int,
            end_name: int,
            expression: RegularExpression
        ) -> Transition:
        """
        Add a transition between two existing states.

        Args:
            start_name (int): The numeric name of the starting state.
            end_name (int): The numeric name of the ending state.
            expression (RegularExpression): The regular expression labeling the transition.

        Raises:
            ValueError: If either the starting or ending state does not exist.

        Returns:
            Transition: The newly created transition.
        """
        if not isinstance(start_name, int) or isinstance(start_name, bool):
            raise TypeError("Start state name must be an integer.")

        if not isinstance(end_name, int) or isinstance(end_name, bool):
            raise TypeError("End state name must be an integer.")

        if not isinstance(expression, RegularExpression):
            raise TypeError("Transition expression must be a RegularExpression.")

        start_state = self.get_state(start_name)
        end_state = self.get_state(end_name)

        if start_state is None or end_state is None:
            raise ValueError("Start or end state does not exist.")

        transition = Transition(start_state, end_state, expression)
        self.transitions.append(transition)
        return transition

    def remove_transition(
            self,
            start_name: int,
            end_name: int
        ) -> None:
        """
        Remove all transitions between two states.

        Args:
            start_name (int): The numeric name of the starting state.
            end_name (int): The numeric name of the ending state.

        Raises:
            ValueError: If no transitions exist between the specified states.
        """
        transitions = self.get_transitions(start_name, end_name)

        if not transitions:
            raise ValueError("No transitions found for the given start and end states.")

        for transition in transitions:
            if transition in self.transitions:
                self.transitions.remove(transition)

    def get_accepting_states(
            self
        ) -> list[State]:
        """
        Find all accepting states in the automaton.

        Returns:
            list[State]: A list containing all of the accepting states.
        """
        return [s for s in self.states if s.is_accepting]

    def get_incoming_transitions(
            self,
            state_name: int
        ) -> list[Transition]:
        """
        Find all non-self-loop transitions entering a state.

        Args:
            state_name (int): The numeric name of the destination state.

        Raises:
            ValueError: If the specified state does not exist.

        Returns:
            list[Transition]: A list of transitions entering the specified state, excluding self-loops.
        """
        state = self.get_state(state_name)

        if state is None:
            raise ValueError("State does not exist.")

        return [t for t in self.transitions if t.end == state and t.start != state]

    def get_outgoing_transitions(
            self,
            state_name: int
        ) -> list[Transition]:
        """
        Find all non-self-loop transitions leaving a state.

        Args:
            state_name (int): The numeric name of the source state.

        Raises:
            ValueError: If the specified state does not exist.

        Returns:
            list[Transition]: The outgoing transitions, excluding self-loops.
        """
        state = self.get_state(state_name)

        if state is None:
            raise ValueError("State does not exist.")

        return [t for t in self.transitions if t.start == state and t.end != state]

    def get_self_loops(
            self,
            state_name: int
        ) -> list[Transition]:
        """
        Find all self-loop transitions on a state.

        Args:
            state_name (int): The numeric name of the state.

        Raises:
            ValueError: If the specified state does not exist.

        Returns:
            list[Transition]: The transitions that start and end at this state.
        """
        state = self.get_state(state_name)

        if state is None:
            raise ValueError("State does not exist.")

        return [t for t in self.transitions if t.start == state and t.end == state]

    @abstractmethod
    def __str__(
            self
        ) -> str:
        """
        Return the automaton in its comma-separated definition format.

        Concrete automaton types must list all state definitions first,
        followed by all transition definitions. Individual states and
        transitions are responsible for formatting their own representations.

        Raises:
            NotImplementedError: If a concrete automaton does not implement
                this method.

        Returns:
            str: The serialized automaton definition.
        """
        raise NotImplementedError(
            "Concrete automata must implement __str__."
        )
