"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

import unittest

from automaton import NFA
from regex import RegularExpression


class TestNFA(unittest.TestCase):
    """
    Check NFA construction, validation, transitions, and formatting.
    """

    def make_basic_nfa(
            self
        ) -> NFA:
        """
        Create a reusable two-state NFA for unit tests.
        """
        nfa = NFA()
        nfa.add_state(0)
        nfa.add_state(1, True)
        nfa.set_start_state(0)
        return nfa

    def test_add_states_and_set_start_state(
            self
        ):
        """
        Verify that states can be added and q0 can be selected as the start.
        """
        nfa = self.make_basic_nfa()

        self.assertEqual([state.name for state in nfa.states], [0, 1])
        self.assertEqual(nfa.start_state.name, 0)
        self.assertEqual([state.name for state in nfa.get_accepting_states()], [1])

    def test_duplicate_state_is_rejected(
            self
        ):
        """
        Verify that two states cannot have the same numeric name.
        """
        nfa = NFA()
        nfa.add_state(0)

        with self.assertRaises(ValueError):
            nfa.add_state(0)

    def test_add_valid_transitions(
            self
        ):
        """
        Verify that a, b, and epsilon transitions can be added.
        """
        nfa = self.make_basic_nfa()
        nfa.add_transition(0, 1, RegularExpression.a())
        nfa.add_transition(0, 1, RegularExpression.b())
        nfa.add_transition(1, 1, RegularExpression.epsilon())

        self.assertEqual(len(nfa.transitions), 3)
        self.assertTrue(nfa.validate_complete())

    def test_parallel_transitions_are_preserved(
            self
        ):
        """
        Verify that NFAs retain separate transitions with matching endpoints.
        """
        nfa = self.make_basic_nfa()
        nfa.add_transition(0, 1, RegularExpression.a())
        nfa.add_transition(0, 1, RegularExpression.b())

        self.assertEqual(len(nfa.get_transitions(0, 1)), 2)

    def test_invalid_transition_expression_is_rejected(
            self
        ):
        """
        Verify that an NFA rejects a compound regular-expression label.
        """
        nfa = self.make_basic_nfa()
        compound_expression = RegularExpression.a().union(RegularExpression.b())

        with self.assertRaises(ValueError):
            nfa.add_transition(0, 1, compound_expression)

    def test_transition_with_missing_state_is_rejected(
            self
        ):
        """
        Verify that transition endpoints must already exist.
        """
        nfa = self.make_basic_nfa()

        with self.assertRaises(ValueError):
            nfa.add_transition(0, 2, RegularExpression.a())

    def test_missing_start_state_fails_validation(
            self
        ):
        """
        Verify that an NFA without a start state is incomplete.
        """
        nfa = NFA()
        nfa.add_state(0)

        self.assertFalse(nfa.validate_complete())

    def test_nonzero_start_state_fails_validation(
            self
        ):
        """
        Verify that the NFA start state must be q0.
        """
        nfa = NFA()
        nfa.add_state(1)
        nfa.set_start_state(1)

        self.assertFalse(nfa.validate_complete())

    def test_nfa_string_lists_states_before_transitions(
            self
        ):
        """
        Verify that NFA string output uses the required comma-separated format.
        """
        nfa = self.make_basic_nfa()
        nfa.add_transition(0, 1, RegularExpression.a())

        self.assertEqual(str(nfa), "q0,q1f,q0-a->q1")

    def test_remove_state_removes_connected_transitions(
            self
        ):
        """
        Verify that removing a state also removes its transitions.
        """
        nfa = self.make_basic_nfa()
        nfa.add_transition(0, 1, RegularExpression.a())

        nfa.remove_state(1)

        self.assertIsNone(nfa.get_state(1))
        self.assertEqual(nfa.transitions, [])
        self.assertTrue(nfa.validate_complete())

    def test_remove_transitions_removes_all_parallel_edges(
            self
        ):
        """
        Verify that removing a pair of endpoints removes every parallel edge.
        """
        nfa = self.make_basic_nfa()
        nfa.add_transition(0, 1, RegularExpression.a())
        nfa.add_transition(0, 1, RegularExpression.b())

        nfa.remove_transition(0, 1)

        self.assertEqual(nfa.get_transitions(0, 1), [])


if __name__ == "__main__":
    unittest.main()
