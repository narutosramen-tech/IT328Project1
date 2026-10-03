"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

from .regex_node import RegexNode
from .regex_symbol import RegexSymbol
from .symbol_node import SymbolNode
from .concat_node import ConcatNode
from .union_node import UnionNode
from .star_node import StarNode


class RegularExpression:
    """
    Represents a regular expression as a tree of RegexNode objects.

    RegularExpression provides the public interface for constructing and
    manipulating regular expressions. Expressions can be created from the
    symbols a, b, epsilon, and the empty set, and may be combined using
    union, concatenation, and Kleene star operations.

    The internal RegexNode tree is responsible for preserving expression
    structure and correctly formatting the expression as a string.

    Attributes:
        root (RegexNode): The root node of the regex expression tree.
    """
    root: RegexNode

    def __init__(
            self,
            root: RegexNode
        ) -> None:
        """
        Create a RegularExpression with the given RegexNode as its root.

        DO NOT CALL THIS CONSTRUCTOR DIRECTLY. Use the factory methods instead.

        Args:
            root (RegexNode): The root node of the regular expression tree.

        Raises:
            TypeError: If root is not an instance of RegexNode.
        """
        if not isinstance(root, RegexNode):
            raise TypeError("Root must be an instance of RegexNode")

        self.root = root

    # ----------- Factory Methods -----------

    @classmethod
    def a(
            cls
        ) -> 'RegularExpression':
        """
        Create a regular expression representing the symbol 'a'.

        Returns:
            RegularExpression: A RegularExpression containing the symbol 'a'.
        """
        return cls(SymbolNode(RegexSymbol.A))

    @classmethod
    def b(
            cls
        ) -> 'RegularExpression':
        """
        Create a regular expression representing the symbol 'b'.

        Returns:
            RegularExpression: A RegularExpression containing the symbol 'b'.
        """
        return cls(SymbolNode(RegexSymbol.B))

    @classmethod
    def epsilon(
            cls
        ) -> 'RegularExpression':
        """
        Create a regular expression representing the empty string.

        Returns:
            RegularExpression: A RegularExpression containing the empty string.
        """
        return cls(SymbolNode(RegexSymbol.EPSILON))

    @classmethod
    def empty_set(
            cls
        ) -> 'RegularExpression':
        """
        Create a regular expression representing the empty set.

        Returns:
            RegularExpression: A RegularExpression containing the empty set.
        """
        return cls(SymbolNode(RegexSymbol.EMPTY_SET))

    # ---------- Regex Operations -----------

    def union(
            self,
            other: 'RegularExpression'
        ) -> 'RegularExpression':
        """
        Create the union of this regular expression and another expression.

        The operation performs basic simplification using the identities:
        EmptySet U R = R, R U EmptySet = R, and R U R = R. Nested union
        operands are flattened so duplicate alternatives are not repeated.

        Args:
            other (RegularExpression): The RegularExpression to union with this expression.

        Raises:
            TypeError: If other is not an instance of RegularExpression.

        Returns:
            RegularExpression: A RegularExpression representing the union of the two expressions.
        """
        if not isinstance(other, RegularExpression):
            raise TypeError("Other must be an instance of RegularExpression")

        def collect_union_terms(
                node: RegexNode
            ) -> list[RegexNode]:
            """Flatten nested union nodes into their individual terms."""
            if isinstance(node, UnionNode):
                return (
                    collect_union_terms(node.left)
                    + collect_union_terms(node.right)
                )

            return [node]

        terms = collect_union_terms(self.root) + collect_union_terms(other.root)
        unique_terms: list[RegexNode] = []

        for term in terms:
            expression = RegularExpression(term)

            if expression.is_empty_set():
                continue

            if not any(expression == RegularExpression(existing) for existing in unique_terms):
                unique_terms.append(term)

        if not unique_terms:
            return RegularExpression.empty_set()

        result = RegularExpression(unique_terms[0])

        for term in unique_terms[1:]:
            result = RegularExpression(
                UnionNode(result.root, term)
            )

        return result

    def concatenate(
            self,
            other: 'RegularExpression'
        ) -> 'RegularExpression':
        """
        Concatenate this regular expression with another expression.

        The operation performs basic simplification using the identities:
        EmptySet . R = EmptySet, R . EmptySet = EmptySet,
        epsilon . R = R, and R . epsilon = R.

        Args:
            other (RegularExpression): The RegularExpression to concatenate after this expression.

        Raises:
            TypeError: If other is not an instance of RegularExpression.

        Returns:
            RegularExpression: A RegularExpression representing the concatenation.
        """
        if not isinstance(other, RegularExpression):
            raise TypeError("Other must be an instance of RegularExpression")

        # Empty set . R = Empty set
        if self.is_empty_set() or other.is_empty_set():
            return RegularExpression.empty_set()

        # empty string . R = R
        if self.is_epsilon():
            return other

        # R . empty string = R
        if other.is_epsilon():
            return self

        return RegularExpression(
            ConcatNode(self.root, other.root)
        )

    def kleene_star(
            self
        ) -> 'RegularExpression':
        """
        Apply the Kleene star operation to this regular expression.

        The operation performs basic simplification using the identities:
        EmptySet* = epsilon, epsilon* = epsilon, and (R*)* = R*.

        Returns:
            RegularExpression: A RegularExpression representing the Kleene star of this expression.
        """
        # Empty set* = epsilon
        if self.is_empty_set():
            return RegularExpression.epsilon()

        # epsilon* = epsilon
        if self.is_epsilon():
            return RegularExpression.epsilon()

        # (R*)* = R*
        if isinstance(self.root, StarNode):
            return self

        return RegularExpression(
            StarNode(self.root)
        )

    # ---------- Helper Methods -----------

    def is_epsilon(
            self
        ) -> bool:
        """
        Determine whether this regular expression represents only epsilon.

        Returns:
            bool: True if the root is the epsilon symbol, False otherwise.
        """
        return (
            isinstance(self.root, SymbolNode)
            and self.root.symbol == RegexSymbol.EPSILON
        )

    def is_empty_set(
            self
        ) -> bool:
        """
        Determine whether this regular expression represents the empty set.

        Returns:
            bool: True if the root is the empty set symbol, False otherwise.
        """
        return (
            isinstance(self.root, SymbolNode)
            and self.root.symbol == RegexSymbol.EMPTY_SET
        )

    # ---------- String Representation -----------

    def __str__(
            self
        ) -> str:
        """
        Convert this regular expression to its formatted string representation.

        Returns:
            str: The regular expression represented as a string.
        """
        return str(self.root)

    # ---------- Equality Check -----------

    def __eq__(
            self,
            other: object
        ) -> bool:
        """
        Determine whether this regular expression is structurally equal to another.

        Equality is determined by comparing the root nodes of the two expression
        trees. Individual RegexNode subclasses determine equality for their own
        structures.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True if other is an equivalent RegularExpression tree, False otherwise.
        """
        if not isinstance(other, RegularExpression):
            return False

        return self.root == other.root

    # ---------- Representation -----------

    def __repr__(
            self
        ) -> str:
        """
        Return a developer-oriented representation of this regular expression.

        Returns:
            str: A string representation suitable for debugging.
        """
        return f"RegularExpression({repr(self.root)})"
