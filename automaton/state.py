"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""


class State:
    """
    Represents a state in an automaton.

    Attributes:
        name(int): The name of the state, e.g. q0, q11, qNumber
        is_accepting(bool): Whether the state is an accepting state or not.
    """
    name: int
    is_accepting: bool

    def __init__(self, name: int, is_accepting: bool = False) -> None:
        """
        Create a state with the given numberic name and acceptance status.

        Args:
            name (int): The numeric identifier of the state.
            is_accepting (bool, optional): True if the state is accepting,
            False otherwise. Defaults to False.
        """
        self.name = name
        self.is_accepting = is_accepting

    def __str__(self) -> str:
        """
        Return the state in the assignment's required string format.

        Accepting states are written with an 'f' suffix, such as q2f.
        Non-accepting states are written without the suffix, such as q2.

        Returns:
            str: The formatted state name.
        """
        result = f"q{self.name}"
        if self.is_accepting:
            result += "f"
        return result

    def __eq__(self, other: object) -> bool:
        """
        Determine whether this state is equal to another state.

        State equality is based only on the numeric state name.
        Acceptance status is not considered because q0 and q0f represent
        the same logical state with different acceptance status.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True if the other State has teh same numeric name,
                otherwise NotImplemented for unsupported types.
        """
        if not isinstance(other, State):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        """
        Return a hash value based on the state's numeric name.

        The hash uses only the state name so that it remains consistent
        with the equality definition.

        Returns:
            int: The hash value for this state.
        """
        return hash(self.name)
