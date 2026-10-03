"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
AI was asked about missing edge cases, or testing criteria, to verify thorough unit testing.
"""

import unittest

from automaton import GNFA
from automaton import NFA
from automaton import NFAToGNFAConverter
from regex import RegularExpression


class TestGNFA(unittest.TestCase):
    """
    Check NFA-to-GNFA conversion and GNFA structural validation.
    """

    def make_basic_nfa(
            self
        ) -> NFA:
        """
        Create a valid two-state NFA for GNFA conversion tests.
        """
        nfa = NFA()
        nfa.add_state(0)
        nfa.add_state(1, True)
        nfa.set_start_state(0)
        return nfa

    def test_conversion_adds_boundary_states(
            self
        ):
        """
        Verify that the first two free numbers become boundary states.
        """
        nfa = self.make_basic_nfa()
        nfa.add_transition(0, 1, RegularExpression.a())

        gnfa = GNFA.from_nfa(nfa)

        self.assertEqual(gnfa.start_state.name, 2)
        self.assertEqual(gnfa.new_accept_state.name, 3)
        self.assertEqual(len(gnfa.get_accepting_states()), 1)
        self.assertEqual(gnfa.get_accepting_states()[0].name, 3)
        self.assertTrue(gnfa.validate_complete())

    def test_converter_wrapper_returns_gnfa(
            self
        ):
        """
        Verify that the public converter wrapper delegates to GNFA creation.
        """
        nfa = self.make_basic_nfa()
        nfa.add_transition(0, 1, RegularExpression.a())

        gnfa = NFAToGNFAConverter.convert(nfa)

        self.assertIsInstance(gnfa, GNFA)
        self.assertTrue(gnfa.validate_complete())

    def test_conversion_adds_boundary_epsilon_transitions(
            self
        ):
        """
        Verify that boundary states connect to the old start and accept states.
        """
        nfa = self.make_basic_nfa()
        nfa.add_transition(0, 1, RegularExpression.a())

        gnfa = GNFA.from_nfa(nfa)

        start_edge = gnfa.get_transitions(2, 0)[0]
        accept_edge = gnfa.get_transitions(1, 3)[0]

        self.assertTrue(start_edge.expression.is_epsilon())
        self.assertTrue(accept_edge.expression.is_epsilon())
        self.assertFalse(gnfa.get_state(1).is_accepting)

    def test_parallel_transitions_are_unioned(
            self
        ):
        """
        Verify that parallel NFA transitions become one union-labeled edge.
        """
        nfa = self.make_basic_nfa()
        nfa.add_transition(0, 1, RegularExpression.a())
        nfa.add_transition(0, 1, RegularExpression.b())

        gnfa = GNFA.from_nfa(nfa)
        transitions = gnfa.get_transitions(0, 1)

        self.assertEqual(len(transitions), 1)
        self.assertEqual(str(transitions[0].expression), "aUb")

    def test_missing_inner_edges_use_empty_set(
            self
        ):
        """
        Verify that missing inner-state transitions receive es labels.
        """
        nfa = self.make_basic_nfa()
        gnfa = GNFA.from_nfa(nfa)

        self.assertTrue(gnfa.get_transitions(0, 0)[0].expression.is_empty_set())
        self.assertTrue(gnfa.get_transitions(1, 0)[0].expression.is_empty_set())

    def test_old_nfa_is_not_mutated(
            self
        ):
        """
        Verify that conversion does not change the original NFA states.
        """
        nfa = self.make_basic_nfa()
        nfa.add_transition(0, 1, RegularExpression.a())

        GNFA.from_nfa(nfa)

        self.assertEqual([state.name for state in nfa.get_accepting_states()], [1])
        self.assertEqual(str(nfa), "q0,q1f,q0-a->q1")

    def test_incomplete_nfa_is_rejected(
            self
        ):
        """
        Verify that conversion rejects an NFA without a start state.
        """
        nfa = NFA()
        nfa.add_state(0)

        with self.assertRaises(ValueError):
            GNFA.from_nfa(nfa)

    def test_non_nfa_conversion_input_is_rejected(
            self
        ):
        """
        Verify that GNFA conversion requires an NFA instance.
        """
        with self.assertRaises(TypeError):
            GNFA.from_nfa(None)  # type: ignore[arg-type]

    def test_combine_transitions_rejects_empty_input(
            self
        ):
        """
        Verify that combining an empty transition list is rejected.
        """
        gnfa = GNFA()

        with self.assertRaises(ValueError):
            gnfa.combine_transitions([])


if __name__ == "__main__":
    unittest.main()
