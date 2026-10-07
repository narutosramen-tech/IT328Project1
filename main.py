"""
Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

All code was written by students and all comments were written by AI.
"""

import sys
from automaton import NFAParser, NFAToGNFAConverter
from automaton import GNFAParser, GNFAToRegexConverter

print("1. NFA to GNFA")
print("2. GNFA to regular expression")

choice = input("Choose 1 or 2: ")

if choice != "1" and choice != "2":
    print("Choose 1 or 2.")
    sys.exit(1)

machine = input("Enter the machine: ")

try:
    if choice == "1":
        # Read the NFA, convert it to a GNFA, and print the result.
        nfa = NFAParser(machine).parse()
        gnfa = NFAToGNFAConverter.convert(nfa)
        print(gnfa)

    # Read the GNFA, convert it to a regex, and print the result.
    elif choice == "2":
        gnfa = GNFAParser(machine).parse()
        regex = GNFAToRegexConverter.convert(gnfa)
        print(regex)


except ValueError as error:
    print("Error:", error, file=sys.stderr)
    sys.exit(1)