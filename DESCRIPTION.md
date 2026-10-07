1. Overall architecture
The program has four main layers:
main.py
   ↓
Parsers and converters
   ↓
NFA/GNFA automaton models
   ↓
Regular-expression representation and operations
The complete processing pipeline is:
NFA input string
    ↓
NFAParser
    ↓
NFA object
    ↓
NFAToGNFAConverter
    ↓
GNFA object
    ↓
GNFAToRegexConverter
    ↓
RegularExpression object
    ↓
Formatted regular-expression string
A GNFA can also be parsed directly using GNFAParser.
2. Entry point
main.py
This is the executable user interface.
It:
- Displays the two available operations.
- Accepts an NFA or GNFA definition from the user.
- Uses NFAParser for NFA input.
- Uses NFAToGNFAConverter for NFA-to-GNFA conversion.
- Uses GNFAParser for GNFA input.
- Uses GNFAToRegexConverter for GNFA-to-regex conversion.
- Prints results to standard output.
- Prints errors to standard error.
- Exits with a nonzero status when invalid input is supplied.
There are no classes in this module.
3. automaton package
The automaton package contains the state-machine data structures, parsers, and conversion algorithms.
automaton/state.py
State
Represents one state in an automaton.
Important responsibilities:
- Stores a nonnegative numeric state name.
- Stores whether the state is accepting.
- Formats states as q0, q1, or q2f.
- Supports equality and hashing based on the numeric state name.
Acceptance is not part of state identity. Therefore, q2 and q2f refer to the same numbered state with different acceptance status.
automaton/transition.py
Transition
Represents a directed edge between two states.
Each transition contains:
- A starting State.
- An ending State.
- A RegularExpression label.
It formats transitions as:
q0-a->q1
The class also validates that endpoints are State objects and that the label is a RegularExpression.
automaton/automaton.py
Automaton
An abstract base class shared by NFA and GNFA.
It stores:
- A list of states.
- A list of transitions.
- A start state.
Common operations include:
- Adding and finding states.
- Setting the start state.
- Removing states.
- Adding and removing transitions.
- Finding accepting states.
- Finding incoming transitions.
- Finding outgoing transitions.
- Finding self-loops.
- Formatting the automaton.
The class leaves __str__() abstract because NFAs and GNFAs have slightly different formatting and structural rules.
automaton/nfa.py
NFA
Represents a nondeterministic finite automaton.
It inherits the general storage and manipulation behavior from Automaton.
Additional NFA responsibilities:
- Restricts transition labels to:
  - a
  - b
  - e, representing epsilon
- Allows multiple transitions between the same pair of states.
- Requires q0 to be the start state.
- Validates that all transition endpoints belong to the NFA.
- Formats states before transitions.
An NFA can have multiple accepting states.
automaton/gnfa.py
GNFA
Represents a generalized nondeterministic finite automaton whose transitions are labeled with regular expressions.
Additional GNFA responsibilities:
- Stores copied inner states from the original NFA.
- Stores a new start state.
- Stores a new accepting state.
- Ensures exactly one accepting state exists.
- Ensures every ordered pair of inner states has exactly one transition.
- Uses es to represent missing transitions.
- Combines parallel transitions using union.
For example:
q0-a->q1
q0-b->q1
becomes:
q0-aUb->q1
The GNFA class also:
- Adds epsilon transitions from the new start state.
- Adds epsilon transitions from old accepting states to the new accepting state.
- Removes accepting status from old accepting states.
- Preserves the original NFA by copying its states and transitions.
automaton/nfa_parser.py
NFAParser
Converts an NFA definition string into an NFA object.
It supports:
- State declarations such as q0 and q1f.
- Transitions such as q0-a->q1.
- Epsilon transitions such as q0-e->q1.
- Whitespace-insensitive input.
- Multiple accepting states.
- Parallel transitions.
It rejects:
- Empty input.
- Invalid state names.
- Duplicate states.
- Transitions involving undeclared states.
- Accepting markers on transition endpoints.
- Unsupported transition labels.
- NFAs without q0.
automaton/gnfa_parser.py
GNFAParser
Converts a normalized GNFA definition string into a GNFA object.
It determines the GNFA structure using declaration order:
- The first declared state is the start state.
- The final declared state must be the accepting state.
- States in between are inner states.
It parses regular-expression labels containing:
- a
- b
- e
- es
- Union using U
- Implicit concatenation
- Kleene star using *
- Parentheses
The parser uses nested parsing functions to enforce operator precedence:
Kleene star
    ↓
Concatenation
    ↓
Union
It also rejects malformed expressions, duplicate state-pair transitions, undeclared endpoints, and invalid GNFA structures.
automaton/nfa_to_gnfa_converter.py
NFAToGNFAConverter
Provides the public conversion interface for converting an NFA into a GNFA.
Its convert() method:
1. Validates that the input is an NFA.
2. Validates the NFA structure.
3. Calls GNFA.from_nfa().
4. Returns a normalized GNFA.
The actual construction logic is implemented by the GNFA class.
automaton/gnfa_to_regex_converter.py
GNFAToRegexConverter
Converts a normalized GNFA into an equivalent regular expression.
It implements state elimination.
For each eliminated state k, it updates paths using:
Rij = Rij U Rik(Rkk)*Rkj
The converter:
- Leaves the start and accepting states until the end.
- Eliminates every inner state.
- Handles loops using Kleene star.
- Handles missing paths using es.
- Preserves direct paths while adding paths through eliminated states.
- Does not modify the original GNFA.
- Returns the final start-to-accept expression.
automaton/__init__.py
This package initializer exposes the main automaton classes and conversion tools:
- Automaton
- NFA
- GNFA
- NFAParser
- NFAToGNFAConverter
- GNFAParser
- GNFAToRegexConverter
This allows callers to import public classes from the package, for example:
from automaton import NFAParser
4. regex package
The regex package represents regular expressions as trees rather than plain strings. This allows the program to simplify expressions and format parentheses correctly.
regex/regular_expression.py
RegularExpression
This is the main public regular-expression class.
It provides factory methods for:
- a
- b
- epsilon
- empty_set
It also provides operations for:
- Union
- Concatenation
- Kleene star
- Equality
- String formatting
The class performs simplifications such as:
es U R = R
R U R = R
esR = es
eR = R
R* = R*
It is used throughout the automaton package to label transitions and construct the final result.
regex/regex_symbol.py
RegexSymbol
An enumeration of supported atomic symbols:
- A, rendered as a
- B, rendered as b
- EPSILON, rendered as e
- EMPTY_SET, rendered as es
This centralizes the legal literal symbols used by the expression system.
regex/regex_node.py
RegexNode
An abstract base class for all expression-tree nodes.
It defines the interface for:
- String conversion.
- Developer-oriented representations.
- Precedence comparison.
The concrete node classes inherit from it.
regex/symbol_node.py
SymbolNode
Represents one atomic expression symbol.
Examples include:
a
b
e
es
It is the leaf node in a regular-expression tree.
regex/binary_node.py
BinaryNode
A base class for operators with two operands.
It stores:
- A left child.
- A right child.
It is inherited by:
- ConcatNode
- UnionNode
regex/unary_node.py
UnaryNode
A base class for operators with one operand.
It stores a single child expression.
It is inherited by:
- StarNode
regex/concat_node.py
ConcatNode
Represents implicit concatenation.
For example:
ab
It has higher precedence than union, so it can format expressions such as:
a(bUc)
with the necessary parentheses.
regex/union_node.py
UnionNode
Represents union using uppercase U.
For example:
aUb
Union has the lowest precedence among the supported operators.
The class also treats union operands as unordered for equality comparisons, so aUb and bUa are considered equivalent structurally.
regex/star_node.py
StarNode
Represents the Kleene star operation.
Examples include:
a*
(aUb)*
It has the highest operator precedence and adds parentheses around lower-precedence operands when necessary.
regex/stringable.py
Stringable
Defines a common interface for classes that provide a string representation.
It requires subclasses to implement __str__().
regex/precedence_aware.py
PrecedenceAware
Defines the interface used to compare operator precedence.
The expression nodes use precedence values to determine when parentheses are required during formatting.
regex/__init__.py
This package initializer exposes RegularExpression as the main public interface:
from regex import RegularExpression
The rest of the expression-tree classes are internal implementation details used by RegularExpression.
5. How the classes work together
The primary relationships are:
State ───────┐
             ├── Transition
RegularExpression ─┘

Automaton
   ├── NFA
   └── GNFA

NFAParser ───────────────> NFA
NFAToGNFAConverter ──────> GNFA
GNFAParser ───────────────> GNFA
GNFAToRegexConverter ────> RegularExpression
A transition connects two states and uses a regular expression as its label. NFAs restrict those expressions to single symbols or epsilon, while GNFAs allow complete regular expressions.
The conversion process is therefore:
1. NFAParser creates states and transitions.
2. NFA validates the automaton.
3. NFAToGNFAConverter creates a normalized GNFA.
4. GNFA combines parallel edges and adds missing es edges.
5. GNFAToRegexConverter eliminates inner states.
6. RegularExpression simplifies and formats the final result.
6. Test modules
The project also contains unittest modules that verify the implementation.
Test module	Test class	Main purpose
tests/test_nfa.py	TestNFA	Tests states, transitions, validation, and NFA formatting
tests/test_nfa_parser.py	TestNFAParser	Tests valid and invalid NFA parsing
tests/test_gnfa.py	TestGNFA	Tests GNFA construction, normalization, and validation
tests/test_nfa_to_gnfa.py	TestNFAToGNFA	Tests conversion edge cases such as loops and multiple accepting states
tests/test_gnfa_parser.py	TestGNFAParser	Tests GNFA and regular-expression parsing
tests/test_gnfa_to_regex.py	TestGNFAToRegex	Tests state elimination and generated expressions
tests/test_regular_expressions.py	TestRegularExpressions	Tests regex construction, simplification, equality, and precedence
tests/test_nfa_to_regex_integration.py	TestNFAToRegexIntegration	Tests the complete NFA-to-regex pipeline



The tests collectively verify the program’s parsing, validation, conversion, regular-expression construction, formatting, and end-to-end behavior.