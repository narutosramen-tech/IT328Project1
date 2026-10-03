"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

import unittest

from automaton import NFAToGNFAConverter
from automaton import NFA
from regex import RegularExpression


class TestNFAToGNFA(unittest.TestCase):
    """
    Check NFA-to-GNFA conversion for accepting states and self-loops.
    """

    def test_multiple_accepting_states_connect_to_new_accept_state(
            self
        ):
        """
        Verify that every old accepting state reaches the new accept state.
        """
        nfa = NFA()
        nfa.add_state(0)
        nfa.add_state(1, True)
        nfa.add_state(2, True)
        nfa.set_start_state(0)
        nfa.add_transition(0, 1, RegularExpression.a())
        nfa.add_transition(0, 2, RegularExpression.b())

        gnfa = NFAToGNFAConverter.convert(nfa)

        new_accept_name = gnfa.new_accept_state.name

        self.assertEqual(len(gnfa.get_accepting_states()), 1)
        self.assertEqual(
            len(gnfa.get_transitions(1, new_accept_name)),
            1
        )
        self.assertEqual(
            len(gnfa.get_transitions(2, new_accept_name)),
            1
        )
        self.assertTrue(
            gnfa.get_transitions(1, new_accept_name)[0].expression.is_epsilon()
        )
        self.assertTrue(
            gnfa.get_transitions(2, new_accept_name)[0].expression.is_epsilon()
        )
        self.assertTrue(gnfa.validate_complete())

    def test_accepting_start_state_connects_to_new_accept_state(
            self
        ):
        """
        Verify that an accepting old start state receives an epsilon edge.
        """
        nfa = NFA()
        nfa.add_state(0, True)
        nfa.set_start_state(0)

        gnfa = NFAToGNFAConverter.convert(nfa)

        new_start_name = gnfa.new_start_state.name
        new_accept_name = gnfa.new_accept_state.name

        self.assertFalse(gnfa.get_state(0).is_accepting)
        self.assertTrue(
            gnfa.get_transitions(new_start_name, 0)[0].expression.is_epsilon()
        )
        self.assertTrue(
            gnfa.get_transitions(0, new_accept_name)[0].expression.is_epsilon()
        )
        self.assertTrue(gnfa.validate_complete())

    def test_self_loop_is_preserved_in_gnfa(
            self
        ):
        """
        Verify that an NFA self-loop remains on the copied GNFA state.
        """
        nfa = NFA()
        nfa.add_state(0)
        nfa.add_state(1, True)
        nfa.set_start_state(0)
        nfa.add_transition(0, 0, RegularExpression.a())
        nfa.add_transition(0, 1, RegularExpression.b())

        gnfa = NFAToGNFAConverter.convert(nfa)

        self_loop = gnfa.get_transitions(0, 0)

        self.assertEqual(len(self_loop), 1)
        self.assertEqual(str(self_loop[0].expression), "a")
        self.assertTrue(gnfa.validate_complete())


if __name__ == "__main__":
    unittest.main()
