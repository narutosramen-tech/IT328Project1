"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
AI was asked about missing edge cases, or testing criteria, to verify thorough unit testing.
"""

import unittest

from regex import RegularExpression


class TestRegularExpressions(unittest.TestCase):
    """
    Check expression factories, simplification, rendering, and equality.
    """

    # --------- Factory Method Tests ---------

    def test_a_factory(
            self
        ):
        """
        Verify that the a factory renders as 'a'.
        """
        regex = RegularExpression.a()
        self.assertEqual(str(regex), "a")

    def test_b_factory(
            self
        ):
        """
        Verify that the b factory renders as 'b'.
        """
        regex = RegularExpression.b()
        self.assertEqual(str(regex), "b")

    def test_epsilon_factory(
            self
        ):
        """
        Verify that epsilon renders as 'e'.
        """
        regex = RegularExpression.epsilon()
        self.assertEqual(str(regex), "e")

    def test_empty_set_factory(
            self
        ):
        """
        Verify that the empty set renders as 'es'.
        """
        regex = RegularExpression.empty_set()
        self.assertEqual(str(regex), "es")

    def test_union(
            self
        ):
        """
        Verify that union joins symbols with an uppercase U.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        union_regex = regex1.union(regex2)
        self.assertEqual(str(union_regex), "aUb")

    def test_union_with_empty_set_on_left(
            self
        ):
        """
        Verify that an empty left operand is removed from a union.
        """
        regex1 = RegularExpression.empty_set()
        regex2 = RegularExpression.a()
        union_regex = regex1.union(regex2)
        self.assertEqual(str(union_regex), "a")

    def test_union_with_empty_set_on_right(
            self
        ):
        """
        Verify that an empty right operand is removed from a union.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.empty_set()
        union_regex = regex1.union(regex2)
        self.assertEqual(str(union_regex), "a")

    def test_union_with_itself(
            self
        ):
        """
        Verify that union with the same expression preserves that expression.
        """
        regex = RegularExpression.a()
        union_regex = regex.union(regex)
        self.assertEqual(union_regex, regex)
        self.assertEqual(str(union_regex), "a")

    def test_union_equality_is_commutative(
            self
        ):
        """
        Verify that reversing union operands preserves equality.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        union1 = regex1.union(regex2)
        union2 = regex2.union(regex1)
        self.assertEqual(union1, union2)

    # --------- Concatenation Tests ---------

    def test_concatenation(
            self
        ):
        """
        Verify that concatenation renders operands in order.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "ab")

    def test_concatenation_with_empty_set_on_left(
            self
        ):
        """
        Verify that concatenation with an empty left operand is empty.
        """
        regex1 = RegularExpression.empty_set()
        regex2 = RegularExpression.a()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "es")

    def test_concatenation_with_empty_set_on_right(
            self
        ):
        """
        Verify that concatenation with an empty right operand is empty.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.empty_set()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "es")

    def test_concatenation_with_both_empty_sets(
            self
        ):
        """
        Verify that concatenating two empty sets produces the empty set.
        """
        regex1 = RegularExpression.empty_set()
        regex2 = RegularExpression.empty_set()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "es")

    def test_concatenation_with_epsilon_on_left(
            self
        ):
        """
        Verify that a leading epsilon is removed from concatenation.
        """
        regex1 = RegularExpression.epsilon()
        regex2 = RegularExpression.a()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "a")

    def test_concatenation_with_epsilon_on_right(
            self
        ):
        """
        Verify that a trailing epsilon is removed from concatenation.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.epsilon()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "a")

    def test_concatenation_with_both_epsilons(
            self
        ):
        """
        Verify that concatenating two epsilons produces epsilon.
        """
        regex1 = RegularExpression.epsilon()
        regex2 = RegularExpression.epsilon()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "e")

    # --------- Kleene Star Tests ---------

    def test_kleene_star(
            self
        ):
        """
        Verify that Kleene star appends an asterisk to a symbol.
        """
        regex = RegularExpression.a()
        star_regex = regex.kleene_star()
        self.assertEqual(str(star_regex), "a*")

    def test_kleene_star_of_empty_set(
            self
        ):
        """
        Verify that the star of the empty set simplifies to epsilon.
        """
        regex = RegularExpression.empty_set()
        star_regex = regex.kleene_star()
        self.assertEqual(str(star_regex), "e")

    def test_kleene_star_of_epsilon(
            self
        ):
        """
        Verify that the star of epsilon simplifies to epsilon.
        """
        regex = RegularExpression.epsilon()
        star_regex = regex.kleene_star()
        self.assertEqual(str(star_regex), "e")

    def test_double_kleene_star(
            self
        ):
        """
        Verify that applying star twice preserves a single star.
        """
        regex = RegularExpression.a()
        star_regex = regex.kleene_star()
        double_star_regex = star_regex.kleene_star()
        self.assertEqual(str(double_star_regex), "a*")

    # --------- Parenthesis / Precedence Tests ---------

    def test_star_of_union_uses_parentheses(
            self
        ):
        """
        Verify that star parenthesizes a union operand.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        union_regex = regex1.union(regex2)
        star_regex = union_regex.kleene_star()
        self.assertEqual(str(star_regex), "(aUb)*")

    def test_star_of_concatenation_uses_parentheses(
            self
        ):
        """
        Verify that star parenthesizes a concatenation operand.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        concat_regex = regex1.concatenate(regex2)
        star_regex = concat_regex.kleene_star()
        self.assertEqual(str(star_regex), "(ab)*")

    def test_concat_with_union_on_left_uses_parentheses(
            self
        ):
        """
        Verify that concatenation parenthesizes a left union operand.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        union_regex = regex1.union(regex2)
        concat_regex = union_regex.concatenate(regex1)
        self.assertEqual(str(concat_regex), "(aUb)a")

    def test_concat_with_union_on_right_uses_parentheses(
            self
        ):
        """
        Verify that concatenation parenthesizes a right union operand.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        union_regex = regex1.union(regex2)
        concat_regex = regex1.concatenate(union_regex)
        self.assertEqual(str(concat_regex), "a(aUb)")

    def test_union_does_not_use_parentheses(
            self
        ):
        """
        Verify that union renders concatenation without extra parentheses.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        concat_regex = regex2.concatenate(regex1)
        union_regex = regex1.union(concat_regex)
        self.assertEqual(str(union_regex), "aUba")

    def test_nested_union_removes_duplicate_alternatives(
            self
        ):
        """
        Verify that nested unions flatten and remove duplicate alternatives.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        nested_union = regex2.union(regex1)
        union_regex = regex1.union(nested_union)

        self.assertIn(str(union_regex), ["aUb", "bUa"])

    def test_union_keeps_concat_and_star_operands_intact(
            self
        ):
        """
        Verify that concatenation and star remain individual union operands.
        """
        symbol = RegularExpression.a()
        concatenation = RegularExpression.b().concatenate(symbol)
        star = RegularExpression.b().kleene_star()

        union_regex = symbol.union(concatenation).union(star)

        self.assertEqual(str(union_regex), "aUbaUb*")

    def test_concat_does_not_use_parentheses(
            self
        ):
        """
        Verify that concatenation renders star without extra parentheses.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        star_regex = regex1.kleene_star()
        concat_regex = star_regex.concatenate(regex2)
        self.assertEqual(str(concat_regex), "a*b")

    # --------- Equality Tests ---------

    def test_identical_expressions_are_equal(
            self
        ):
        """
        Verify that matching concatenation trees compare equal.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.a()
        concat1 = regex1.concatenate(regex2)
        concat2 = regex1.concatenate(regex2)
        self.assertEqual(concat1, concat2)

    def test_different_expressions_are_not_equal(
            self
        ):
        """
        Verify that reversing distinct concatenation operands changes equality.
        """
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        concat1 = regex1.concatenate(regex2)
        concat2 = regex2.concatenate(regex1)
        self.assertNotEqual(concat1, concat2)

    # --------- Type Validation Tests ---------

    def test_union_rejects_non_regular_expression(
            self
        ):
        """
        Verify that union rejects an operand that is not a RegularExpression.
        """
        with self.assertRaises(TypeError):
            RegularExpression.a().union("b")  # type: ignore[arg-type]

    def test_concat_rejects_non_regular_expression(
            self
        ):
        """
        Verify that concatenation rejects an invalid operand type.
        """
        with self.assertRaises(TypeError):
            RegularExpression.a().concatenate("b")  # type: ignore[arg-type]

    def test_constructor_rejects_non_regexnode(
            self
        ):
        """
        Verify that construction rejects a root that is not a RegexNode.
        """
        with self.assertRaises(TypeError):
            RegularExpression("a")  # type: ignore[arg-type]

    def test_equality_with_non_regular_expression_returns_false(
            self
        ):
        """
        Verify that comparison with a different object type returns False.
        """
        self.assertFalse(RegularExpression.a() == "a")

    def test_is_epsilon_detects_epsilon_expression(
            self
        ):
        """
        Verify that epsilon detection distinguishes epsilon from a symbol.
        """
        self.assertTrue(RegularExpression.epsilon().is_epsilon())
        self.assertFalse(RegularExpression.a().is_epsilon())

    def test_is_empty_set_detects_empty_set_expression(
            self
        ):
        """
        Verify that empty-set detection distinguishes it from a symbol.
        """
        self.assertTrue(RegularExpression.empty_set().is_empty_set())
        self.assertFalse(RegularExpression.a().is_empty_set())


if __name__ == "__main__":
    unittest.main()
