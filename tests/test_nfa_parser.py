"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

import unittest

from automaton import NFAParser


class TestNFAParser(unittest.TestCase):
    """
    Check parsing of valid and invalid NFA definition strings.
    """

    def test_parse_minimal_nfa(
            self
        ):
        """
        Verify that a minimal NFA with one transition is parsed correctly.
        """
        nfa = NFAParser("q0,q1f,q0-a->q1").parse()

        self.assertEqual(len(nfa.states), 2)
        self.assertEqual(nfa.start_state.name, 0)
        self.assertEqual(len(nfa.get_accepting_states()), 1)
        self.assertEqual(str(nfa), "q0,q1f,q0-a->q1")

    def test_parse_ignores_whitespace(
            self
        ):
        """
        Verify that whitespace can appear between definition components.
        """
        nfa = NFAParser(" q0, q1f, q0 - a -> q1 ").parse()

        self.assertEqual(str(nfa), "q0,q1f,q0-a->q1")

    def test_parser_rejects_non_string_input(
            self
        ):
        """
        Verify that the parser requires a string input definition.
        """
        with self.assertRaises(TypeError):
            NFAParser(None).parse()  # type: ignore[arg-type]

    def test_parser_rejects_empty_input(
            self
        ):
        """
        Verify that an empty definition is rejected.
        """
        with self.assertRaises(ValueError):
            NFAParser("   ").parse()

    def test_parse_multiple_accepting_states(
            self
        ):
        """
        Verify that multiple accepting state declarations are preserved.
        """
        nfa = NFAParser("q0,q1f,q2f,q0-a->q1,q0-b->q2").parse()

        accepting_names = [state.name for state in nfa.get_accepting_states()]

        self.assertEqual(accepting_names, [1, 2])
        self.assertEqual(len(nfa.transitions), 2)

    def test_parse_epsilon_transition(
            self
        ):
        """
        Verify that the e label is parsed as an epsilon expression.
        """
        nfa = NFAParser("q0,q1f,q0-e->q1").parse()

        transition = nfa.get_transitions(0, 1)[0]

        self.assertTrue(transition.expression.is_epsilon())

    def test_parse_self_loop(
            self
        ):
        """
        Verify that a transition from a state to itself is accepted.
        """
        nfa = NFAParser("q0,q1f,q0-a->q0,q0-e->q1").parse()

        self.assertEqual(len(nfa.get_self_loops(0)), 1)
        self.assertEqual(str(nfa), "q0,q1f,q0-a->q0,q0-e->q1")

    def test_parse_parallel_transitions_separately(
            self
        ):
        """
        Verify that parallel NFA transitions remain separate after parsing.
        """
        nfa = NFAParser("q0,q1f,q0-a->q1,q0-b->q1").parse()

        transitions = nfa.get_transitions(0, 1)

        self.assertEqual(len(transitions), 2)
        self.assertEqual([str(t.expression) for t in transitions], ["a", "b"])

    def test_parse_rejects_missing_start_state(
            self
        ):
        """
        Verify that an NFA without q0 is rejected.
        """
        with self.assertRaises(ValueError):
            NFAParser("q1f").parse()

    def test_parse_rejects_undeclared_transition_state(
            self
        ):
        """
        Verify that transitions cannot reference undeclared states.
        """
        with self.assertRaises(ValueError):
            NFAParser("q0,q0-a->q1").parse()

    def test_parse_rejects_duplicate_state(
            self
        ):
        """
        Verify that duplicate state declarations are rejected.
        """
        with self.assertRaises(ValueError):
            NFAParser("q0,q0").parse()

    def test_parse_rejects_invalid_state_token(
            self
        ):
        """
        Verify that malformed state names are rejected.
        """
        with self.assertRaises(ValueError):
            NFAParser("state0,q1f").parse()

    def test_parse_rejects_invalid_transition_label(
            self
        ):
        """
        Verify that labels outside a, b, and e are rejected.
        """
        with self.assertRaises(ValueError):
            NFAParser("q0,q1f,q0-c->q1").parse()

    def test_parse_rejects_accepting_transition_endpoint(
            self
        ):
        """
        Verify that accepting markers cannot appear on transition endpoints.
        """
        with self.assertRaises(ValueError):
            NFAParser("q0,q1f,q0-a->q1f").parse()


if __name__ == "__main__":
    unittest.main()
