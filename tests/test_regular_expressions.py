import unittest

from regex import RegularExpression

class TestRegularExpressions(unittest.TestCase):

    # --------- Factory Method Tests ---------

    def test_a_factory(self):
        regex = RegularExpression.a()
        self.assertEqual(str(regex), "a")

    def test_b_factory(self):
        regex = RegularExpression.b()
        self.assertEqual(str(regex), "b")

    def test_epsilon_factory(self):
        regex = RegularExpression.epsilon()
        self.assertEqual(str(regex), "e")

    def test_empty_set_factory(self):
        regex = RegularExpression.empty_set()
        self.assertEqual(str(regex), "es")

    def test_union(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        union_regex = regex1.union(regex2)
        self.assertEqual(str(union_regex), "aUb")

    def test_union_with_empty_set_on_left(self):
        regex1 = RegularExpression.empty_set()
        regex2 = RegularExpression.a()
        union_regex = regex1.union(regex2)
        self.assertEqual(str(union_regex), "a")

    def test_union_with_empty_set_on_right(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.empty_set()
        union_regex = regex1.union(regex2)
        self.assertEqual(str(union_regex), "a")

    def test_union_with_itself(self):
        regex = RegularExpression.a()
        union_regex = regex.union(regex)
        self.assertEqual(union_regex, regex)
        self.assertEqual(str(union_regex), "a")

    def test_union_equality_is_commutative(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        union1 = regex1.union(regex2)
        union2 = regex2.union(regex1)
        self.assertEqual(union1, union2)

    # --------- Concatenation Tests ---------

    def test_concatenation(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "ab")

    def test_concatenation_with_empty_set_on_left(self):
        regex1 = RegularExpression.empty_set()
        regex2 = RegularExpression.a()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "es")

    def test_concatenation_with_empty_set_on_right(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.empty_set()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "es")

    def test_concatenation_with_both_empty_sets(self):
        regex1 = RegularExpression.empty_set()
        regex2 = RegularExpression.empty_set()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "es")

    def test_concatenation_with_epsilon_on_left(self):
        regex1 = RegularExpression.epsilon()
        regex2 = RegularExpression.a()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "a")

    def test_concatenation_with_epsilon_on_right(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.epsilon()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "a")

    def test_concatenation_with_both_epsilons(self):
        regex1 = RegularExpression.epsilon()
        regex2 = RegularExpression.epsilon()
        concat_regex = regex1.concatenate(regex2)
        self.assertEqual(str(concat_regex), "e")

    # --------- Kleene Star Tests ---------

    def test_kleene_star(self):
        regex = RegularExpression.a()
        star_regex = regex.kleene_star()
        self.assertEqual(str(star_regex), "a*")

    def test_kleene_star_of_empty_set(self):
        regex = RegularExpression.empty_set()
        star_regex = regex.kleene_star()
        self.assertEqual(str(star_regex), "e")

    def test_kleene_star_of_epsilon(self):
        regex = RegularExpression.epsilon()
        star_regex = regex.kleene_star()
        self.assertEqual(str(star_regex), "e")

    def test_double_kleene_star(self):
        regex = RegularExpression.a()
        star_regex = regex.kleene_star()
        double_star_regex = star_regex.kleene_star()
        self.assertEqual(str(double_star_regex), "a*")

    # --------- Parenthesis / Precedence Tests ---------

    def test_star_of_union_uses_parentheses(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        union_regex = regex1.union(regex2)
        star_regex = union_regex.kleene_star()
        self.assertEqual(str(star_regex), "(aUb)*")

    def test_star_of_concatenation_uses_parentheses(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        concat_regex = regex1.concatenate(regex2)
        star_regex = concat_regex.kleene_star()
        self.assertEqual(str(star_regex), "(ab)*")

    def test_concat_with_union_on_left_uses_parentheses(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        union_regex = regex1.union(regex2)
        concat_regex = union_regex.concatenate(regex1)
        self.assertEqual(str(concat_regex), "(aUb)a")

    def test_concat_with_union_on_right_uses_parentheses(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        union_regex = regex1.union(regex2)
        concat_regex = regex1.concatenate(union_regex)
        self.assertEqual(str(concat_regex), "a(aUb)")

    def test_union_does_not_use_parentheses(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        concat_regex = regex2.concatenate(regex1)
        union_regex = regex1.union(concat_regex)
        self.assertEqual(str(union_regex), "aUba")

    def test_concat_does_not_use_parentheses(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        star_regex = regex1.kleene_star()
        concat_regex = star_regex.concatenate(regex2)
        self.assertEqual(str(concat_regex), "a*b")

    # --------- Equality Tests ---------

    def test_identical_expressions_are_equal(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.a()
        concat1 = regex1.concatenate(regex2)
        concat2 = regex1.concatenate(regex2)
        self.assertEqual(concat1, concat2)

    def test_different_expressions_are_not_equal(self):
        regex1 = RegularExpression.a()
        regex2 = RegularExpression.b()
        concat1 = regex1.concatenate(regex2)
        concat2 = regex2.concatenate(regex1)
        self.assertNotEqual(concat1, concat2)

    # --------- Type Validation Tests ---------

    def test_union_rejects_non_regular_expression(self):
        with self.assertRaises(TypeError):
            RegularExpression.a().union("b") # type: ignore[arg-type]

    def test_concat_rejects_non_regular_expression(self):
        with self.assertRaises(TypeError):
            RegularExpression.a().concatenate("b") # type: ignore[arg-type]

    def test_constructor_rejects_non_regexnode(self):
        with self.assertRaises(TypeError):
            RegularExpression("a")  # type: ignore[arg-type]

    def test_equality_with_non_regular_expression_returns_false(self):
        self.assertFalse(RegularExpression.a() == "a")

    def test_is_epsilon_detects_epsilon_expression(self):
        self.assertTrue(RegularExpression.epsilon().is_epsilon())
        self.assertFalse(RegularExpression.a().is_epsilon())

    def test_is_empty_set_detects_empty_set_expression(self):
        self.assertTrue(RegularExpression.empty_set().is_empty_set())
        self.assertFalse(RegularExpression.a().is_empty_set())

if __name__ == "__main__":
    unittest.main()
