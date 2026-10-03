"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

import unittest

from automaton import GNFAToRegexConverter
from automaton import GNFAParser
from automaton import NFAParser
from automaton import NFAToGNFAConverter


class TestNFAToRegexIntegration(unittest.TestCase):
    """
    Check the complete NFA-string-to-regular-expression pipeline.
    """

    def test_nfa_definitions_convert_to_regexes(
            self
        ):
        """
        Verify many NFA shapes through parsing, conversion, and elimination.

        Every case asserts the exact generated expression and verifies that
        the result can be parsed back into an equivalent expression tree.
        """
        cases = [
            (
                "direct a", 
                "q0,q1f,q0-a->q1", 
                "a"
            ),
            (
                "direct b", 
                "q0,q1f,q0-b->q1", 
                "b"
            ),
            (
                "direct epsilon", 
                "q0,q1f,q0-e->q1", 
                "e"
            ),
            (
                "accepting start state", 
                "q0f", 
                "e"
            ),
            (
                "simple empty set", 
                "q0,q1f", 
                "es"
            ),
            (
                "complex empty set",
                "q0,q1f,q2,q0-a->q0,q2-b->q2",
                "es"
            ),
            (
                "aa", 
                "q0,q1,q2f,q0-a->q1,q1-a->q2", 
                "aa"
            ),
            (
                "ab", 
                "q0,q1,q2f,q0-a->q1,q1-b->q2", 
                "ab"
            ),
            (
                "ba", 
                "q0,q1,q2f,q0-b->q1,q1-a->q2", 
                "ba"
            ),
            (
                "bb", 
                "q0,q1,q2f,q0-b->q1,q1-b->q2", 
                "bb"
            ),
            (
                "aba", 
                "q0,q1,q2,q3f,q0-a->q1,q1-b->q2,q2-a->q3", 
                "aba"
            ),
            (
                "a or b", 
                "q0,q1f,q0-a->q1,q0-b->q1", 
                "aUb"
            ),
            (
                "a or epsilon", 
                "q0,q1f,q0-a->q1,q0-e->q1", 
                "aUe"
            ),
            (
                "a star", 
                "q0,q1f,q0-a->q0,q0-e->q1", 
                "a*"
            ),
            (
                "b star", 
                "q0,q1f,q0-b->q0,q0-e->q1", 
                "b*"
            ),
            (
                "a star followed by b", 
                "q0,q1f,q0-a->q0,q0-b->q1", 
                "a*b"
            ),
            (
                "a followed by b star", 
                "q0,q1,q2f,q0-a->q1,q1-b->q1,q1-e->q2", 
                "ab*"
            ),
            (
                "choice followed by a",
                "q0,q1,q2f,q0-a->q1,q0-b->q1,q1-a->q2",
                "(aUb)a"
            ),
            (
                "a followed by a choice",
                "q0,q1,q2f,q0-a->q1,q1-b->q2,q1-e->q2",
                "a(bUe)"
            ),
            (
                "choice followed by b",
                "q0,q1,q2f,q0-a->q1,q0-b->q1,q1-b->q2",
                "(aUb)b"
            ),
            (
                "a and ab alternatives",
                "q0,q1,q2f,q0-a->q2,q0-a->q1,q1-b->q2",
                "aUab"
            ),
            (
                "a or b loop",
                "q0,q1f,q0-a->q0,q0-b->q0,q0-e->q1",
                "(aUb)*"
            ),
            (
                "ab loop",
                "q0,q1,q2f,q0-a->q1,q1-b->q0,q0-e->q2",
                "eUa(ba)*b"
            ),
            (
                "epsilon before a",
                "q0,q1,q2f,q0-e->q1,q1-a->q2",
                "a"
            ),
            (
                "epsilon after a",
                "q0,q1,q2f,q0-a->q1,q1-e->q2",
                "a"
            ),
            (
                "unreachable loop",
                "q0,q1f,q2,q0-a->q1,q2-b->q2",
                "a"
            ),
            (
                "multiple unreachable states",
                "q0,q1f,q2,q3,q0-a->q1,q2-b->q2,q3-a->q3",
                "a"
            ),
            (
                "nested path choices",
                "q0,q1,q2,q3f,q0-a->q1,q0-b->q1,q1-b->q2,q1-e->q2,q2-a->q3",
                "(aUb)(bUe)a"
            ),
            (
                "complex cyclic language",
                "q0,q1,q2,q3f,q0-a->q1,q1-b->q2,q2-b->q2,q2-a->q1,q2-a->q3,q3-b->q2,q1-a->q3,q3-a->q1",
                "(aaUab(bUab)*(aUaa))(aaU(bUab)(bUab)*(aUaa))*"
            ),
        ]

        for label, nfa_definition, expected in cases:
            with self.subTest(case=label):
                nfa = NFAParser(nfa_definition).parse()
                converted_gnfa = NFAToGNFAConverter.convert(nfa)
                serialized_gnfa = str(converted_gnfa)
                parsed_gnfa = GNFAParser(serialized_gnfa).parse()
                regex = GNFAToRegexConverter.convert(parsed_gnfa)
                rendered_regex = str(regex)
                reparsed_regex = GNFAParser(
                    "q0,q1f"
                ).parse_regular_expression(rendered_regex)

                self.assertEqual(rendered_regex, str(reparsed_regex))

                self.assertEqual(rendered_regex, expected)

                self.assertNotIn(" ", rendered_regex)


if __name__ == "__main__":
    unittest.main()
