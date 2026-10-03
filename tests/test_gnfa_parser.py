"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

import unittest

from automaton import GNFAParser


class TestGNFAParser(unittest.TestCase):
    """
    Check GNFA state, transition, and regular-expression parsing.
    """

    def test_parse_normalized_gnfa(
            self
        ):
        """
        Verify that the first and final states define the GNFA boundaries.
        """
        definition = "q2,q0,q1,q3f,q2-e->q0,q0-a->q1,q0-es->q0,q1-es->q0,q1-es->q1,q1-e->q3"

        gnfa = GNFAParser(definition).parse()

        self.assertEqual(gnfa.start_state.name, 2)
        self.assertEqual(gnfa.new_start_state.name, 2)
        self.assertEqual(gnfa.new_accept_state.name, 3)
        self.assertEqual([state.name for state in gnfa.inner_states], [0, 1])
        self.assertTrue(gnfa.validate_complete())

    def test_gnfa_format_and_parse_round_trip(
            self
        ):
        """
        Verify that normalized GNFA output can be parsed again.
        """
        definition = "q2,q0,q1,q3f,q2-e->q0,q0-a->q1,q0-es->q0,q1-es->q0,q1-es->q1,q1-e->q3"
        first_gnfa = GNFAParser(definition).parse()
        serialized = str(first_gnfa)
        second_gnfa = GNFAParser(serialized).parse()

        self.assertEqual(second_gnfa.start_state.name, 2)
        self.assertEqual(second_gnfa.new_accept_state.name, 3)
        self.assertEqual(str(second_gnfa), serialized)

    def test_parse_regular_expression_labels(
            self
        ):
        """
        Verify that union, concatenation, star, epsilon, and empty set parse.
        """
        parser = GNFAParser("q0,q1f")

        expressions = {
            "a": "a",
            "es": "es",
            "e": "e",
            "ab": "ab",
            "aUb": "aUb",
            "(aUb)*": "(aUb)*",
        }

        for source, expected in expressions.items():
            with self.subTest(source=source):
                self.assertEqual(str(parser.parse_regular_expression(source)), expected)

    def test_parse_ignores_whitespace(
            self
        ):
        """
        Verify that whitespace is ignored in GNFA definitions.
        """
        gnfa = GNFAParser(
            " q2, q0, q1, q3f, q2 - e -> q0, q0 - a -> q1, "
            "q0 - es -> q0, q1 - es -> q0, q1 - es -> q1, q1 - e -> q3 "
        ).parse()

        self.assertEqual(gnfa.start_state.name, 2)
        self.assertEqual(str(gnfa.get_transitions(0, 1)[0].expression), "a")

    def test_parse_rejects_accepting_inner_state(
            self
        ):
        """
        Verify that only the final declared GNFA state may be accepting.
        """
        with self.assertRaises(ValueError):
            GNFAParser("q2,q0f,q1,q3f").parse()

    def test_parse_rejects_state_after_transition(
            self
        ):
        """
        Verify that all state declarations must precede transitions.
        """
        with self.assertRaises(ValueError):
            GNFAParser("q2,q3f,q2-e->q3,q1").parse()

    def test_parse_rejects_invalid_expression(
            self
        ):
        """
        Verify that malformed regular-expression labels are rejected.
        """
        parser = GNFAParser("q0,q1f")

        with self.assertRaises(ValueError):
            parser.parse_regular_expression("aU")


if __name__ == "__main__":
    unittest.main()
