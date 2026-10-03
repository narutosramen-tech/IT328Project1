"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

import unittest

from automaton import GNFAToRegexConverter
from automaton import NFAToGNFAConverter
from automaton import NFA
from regex import RegularExpression


class TestGNFAToRegex(unittest.TestCase):
    """
    Check GNFA state elimination and final regular-expression output.
    """

    def test_direct_path(
            self
        ):
        """
        Verify that a direct NFA path produces its transition symbol.
        """
        nfa = NFA()
        nfa.add_state(0)
        nfa.add_state(1, True)
        nfa.set_start_state(0)
        nfa.add_transition(0, 1, RegularExpression.a())

        regex = GNFAToRegexConverter.convert(NFAToGNFAConverter.convert(nfa))

        self.assertEqual(str(regex), "a")

    def test_concatenated_path(
            self
        ):
        """
        Verify that sequential transitions produce concatenation.
        """
        nfa = NFA()
        nfa.add_state(0)
        nfa.add_state(1)
        nfa.add_state(2, True)
        nfa.set_start_state(0)
        nfa.add_transition(0, 1, RegularExpression.a())
        nfa.add_transition(1, 2, RegularExpression.b())

        regex = GNFAToRegexConverter.convert(NFAToGNFAConverter.convert(nfa))

        self.assertEqual(str(regex), "ab")

    def test_loop_produces_kleene_star(
            self
        ):
        """
        Verify that a self-loop produces a Kleene-star expression.
        """
        nfa = NFA()
        nfa.add_state(0)
        nfa.add_state(1, True)
        nfa.set_start_state(0)
        nfa.add_transition(0, 0, RegularExpression.a())
        nfa.add_transition(0, 1, RegularExpression.epsilon())

        regex = GNFAToRegexConverter.convert(NFAToGNFAConverter.convert(nfa))

        self.assertEqual(str(regex), "a*")

    def test_no_accepting_path_produces_empty_set(
            self
        ):
        """
        Verify that an unreachable accepting state produces es.
        """
        nfa = NFA()
        nfa.add_state(0)
        nfa.add_state(1, True)
        nfa.set_start_state(0)

        regex = GNFAToRegexConverter.convert(NFAToGNFAConverter.convert(nfa))

        self.assertTrue(regex.is_empty_set())

    def test_conversion_does_not_mutate_gnfa(
            self
        ):
        """
        Verify that state elimination leaves the input GNFA unchanged.
        """
        nfa = NFA()
        nfa.add_state(0)
        nfa.add_state(1, True)
        nfa.set_start_state(0)
        nfa.add_transition(0, 1, RegularExpression.a())
        gnfa = NFAToGNFAConverter.convert(nfa)
        original = str(gnfa)

        GNFAToRegexConverter.convert(gnfa)

        self.assertEqual(str(gnfa), original)


if __name__ == "__main__":
    unittest.main()
