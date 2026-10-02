"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""


class Stringable:
    """
    Declares the string-conversion contract used by regex nodes.

    Any class that behaves like a regex expression must provide a readable
    string representation through __str__.
    """

    def __str__(
            self
        ) -> str:
        """
        Return the object in a human-readable string form.

        Raises:
            NotImplementedError: If the subclass does not override this method.

        Returns:
            str: A string representation of the regular-expression object.
        """
        raise NotImplementedError("Subclasses must implement __str__ method.")
