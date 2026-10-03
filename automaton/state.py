"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""


class State:
    """
    Represents a state in an automaton.

    Attributes:
        name (int): The name of the state, e.g. q0, q11, qNumber
        is_accepting (bool): Whether the state is an accepting state or not.
    """
    name: int
    is_accepting: bool

    def __init__(
            self,
            name: int,
            is_accepting: bool = False
        ) -> None:
        """
        Create a state with the given numeric name and acceptance status.

        Args:
            name (int): The numeric identifier of the state.
            is_accepting (bool, optional): True if the state is accepting,
                False otherwise. Defaults to False.
        """
        self.name = name
        self.is_accepting = is_accepting

    def __str__(
            self
        ) -> str:
        """
        Return the state's default string representation.

        This method is used automatically by Python's built-in ``str``
        function and by string formatting. Accepting states include the
        ``f`` suffix in this default representation.

        Returns:
            str: The formatted state name, such as ``q2`` or ``q2f``.
        """
        return self.to_string()

    def to_string(
            self,
            append_accepting: bool = True
    ) -> str:
        """
        Format the state name with optional accepting-state information.

        Accepting states include an ``f`` suffix when append_accepting is
        True. Set append_accepting to False when only the numeric state name
        is needed, such as when referring to an accepting state in a
        transition endpoint.

        Args:
            append_accepting (bool, optional): Whether to append the ``f``
                suffix when this state is accepting. Defaults to True.

        Returns:
            str: The formatted state name, such as ``q2`` or ``q2f``.
        """
        result = f"q{self.name}"

        if self.is_accepting and append_accepting:
            result += "f"

        return result

    def __eq__(
            self,
            other: object
        ) -> bool:
        """
        Determine whether this state is equal to another state.

        State equality is based only on the numeric state name.
        Acceptance status is not considered because q0 and q0f represent
        the same logical state with different acceptance status.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True for the same numeric name, False for a different name;
                otherwise NotImplemented for unsupported types.
        """
        if not isinstance(other, State):
            return NotImplemented
        return self.name == other.name

    def __hash__(
            self
        ) -> int:
        """
        Return a hash value based on the state's numeric name.

        The hash uses only the state name so that it remains consistent
        with the equality definition.

        Returns:
            int: The hash value for this state.
        """
        return hash(self.name)
