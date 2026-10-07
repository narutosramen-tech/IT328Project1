# NFA/GNFA Conversion Project Report

**Team Members:**  
[Name]  
[Name, if applicable]  
[Name, if applicable]

## Team Member Contributions

[Team member name] was responsible for [describe contribution].

[Team member name] was responsible for [describe contribution].

[Add additional contribution statements as necessary.]

---

# Problem 1: Converting an NFA to a GNFA

## Algorithm Summary

The first program converts a nondeterministic finite automaton (NFA) into a generalized nondeterministic finite automaton (GNFA). The conversion follows the construction specified in the assignment.

The program first parses the input string into an internal representation of an NFA. It then creates a new GNFA containing copies of the original NFA states and transitions. A new start state and a new accepting state are added. An epsilon transition is added from the new start state to the old start state, and epsilon transitions are added from each former accepting state to the new accepting state.

The program then normalizes the transitions between the inner states of the GNFA. If multiple transitions connect the same ordered pair of states, their labels are combined using regular-expression union. If no transition exists between a required pair of inner states, an empty-set transition is added. The resulting automaton is then written using the required GNFA output format.

The major stages of the algorithm are therefore:

1. Parse and validate the input NFA.
2. Copy the original states and transitions.
3. Add a new start state.
4. Add a new accepting state.
5. Connect the new start state to the old start state with epsilon.
6. Connect every old accepting state to the new accepting state with epsilon.
7. Remove accepting status from the original accepting states.
8. Combine parallel transitions using union.
9. Add empty-set transitions wherever a required transition is missing.
10. Format and output the resulting GNFA.

## Parsing the NFA

Input parsing is performed by the `NFAParser` class in `automaton/nfa_parser.py`. The parser separates the comma-delimited input into state declarations and transition declarations.

For example, a state declaration such as:

`q2f`

indicates that state `q2` is an accepting state, while:

`q2`

indicates a nonaccepting state.

Transitions use the form:

`q0-a->q1`

The parser accepts transition labels `a`, `b`, and `e`, where `e` represents the empty string.

While constructing the NFA, the parser also performs validation. It rejects malformed state names, duplicate state declarations, transitions involving undeclared states, unsupported transition symbols, and NFAs that do not contain `q0` as the start state.

The resulting states and transitions are stored in an `NFA` object. `NFA` inherits common state and transition management behavior from the abstract `Automaton` class.

## Converting the NFA

The public interface for the conversion is the `NFAToGNFAConverter` class in `automaton/nfa_to_gnfa_converter.py`.

Its `convert()` method first confirms that the provided object is an NFA and that the NFA has a valid structure. It then delegates the actual construction of the new automaton to `GNFA.from_nfa()`.

The conversion creates copies of the original states and transitions instead of changing the original NFA. This allows the input NFA to remain unchanged after conversion.

### Adding the New Start State

A GNFA must contain a new start state that has no incoming transitions. The program therefore creates a new state and makes it the GNFA's start state.

An epsilon transition is then created from this new start state to the original NFA start state.

Conceptually, if the original NFA begins with:

`q0`

the converted structure contains:

`new_start-e->q0`

The original `q0` remains in the automaton, but it is no longer the GNFA's start state.

### Adding the New Accepting State

The program also creates one new accepting state.

For every accepting state in the original NFA, the program creates an epsilon transition from that state to the new accepting state. The original states then have their accepting status removed.

For example, if both `q1` and `q3` were accepting states in the NFA, the conversion adds transitions equivalent to:

`q1-e->new_accept`

`q3-e->new_accept`

Only the newly created state remains accepting in the resulting GNFA.

### Combining Parallel Transitions

An NFA may contain multiple transitions between the same pair of states. A normalized GNFA instead uses one regular-expression transition between each required ordered pair of states.

For example, suppose the NFA contains:

`q0-a->q1`

and

`q0-b->q1`

The GNFA combines these into the single transition:

`q0-aUb->q1`

where `U` represents regular-expression union.

The program uses the `RegularExpression` class to construct these expressions instead of manually manipulating strings. This makes it possible to preserve the structure and precedence of increasingly complicated regular expressions.

### Adding Empty-Set Transitions

After parallel transitions have been combined, the program checks the required ordered pairs of inner states.

Whenever no transition exists from one inner state to another, it creates a transition labeled `es`, which represents the empty set.

For example, if no path originally exists from `q1` to `q2`, the GNFA receives:

`q1-es->q2`

This completes the normalization required by Problem 1.

## Worked Example

## Worked Example

Consider the following NFA, which is the example input provided in the assignment:

`q0f,q1,q2,q0-b->q0,q0-a->q1,q1-b->q1,q1-a->q0,q1-e->q2`

The `NFAParser` first creates the three states `q0`, `q1`, and `q2`. Because `q0` contains the `f` marker, it is initially an accepting state. The parser also identifies `q0` as the start state, as required by the NFA input format.

The NFA contains the following transitions:

- `q0-b->q0`
- `q0-a->q1`
- `q1-b->q1`
- `q1-a->q0`
- `q1-e->q2`

The conversion then creates two additional states. Because `q0`, `q1`, and `q2` already exist, the program uses `q3` as the new start state and `q4` as the new accepting state.

The first required GNFA change is to connect the new start state to the original start state with an epsilon transition:

`q3-e->q0`

The second required change is to create a single new accepting state. Since `q0` was accepting in the original NFA, the program removes its accepting status and creates the following epsilon transition:

`q0-e->q4`

State `q4` is then marked as the only accepting state.

At this point, the inner states of the GNFA are `q0`, `q1`, and `q2`. The program examines every ordered pair of these inner states. Existing transitions are retained, while pairs that have no transition are given an empty-set transition represented by `es`.

For `q0`, transitions already exist to `q0` and `q1`, but no transition exists from `q0` to `q2`. Therefore, the program adds:

`q0-es->q2`

For `q1`, transitions already exist to all three inner states:

- `q1-a->q0`
- `q1-b->q1`
- `q1-e->q2`

Therefore, no empty-set transitions need to be added from `q1`.

State `q2` originally has no outgoing transitions to any inner state. The program therefore adds:

- `q2-es->q0`
- `q2-es->q1`
- `q2-es->q2`

The final GNFA produced by the program is:

`q3,q0,q1,q2,q4f,q0-b->q0,q0-a->q1,q1-b->q1,q1-a->q0,q1-e->q2,q3-e->q0,q0-e->q4,q0-es->q2,q2-es->q0,q2-es->q1,q2-es->q2`

This output satisfies the three requirements of the conversion. `q3` is the new start state and has an epsilon transition to the old start state, `q4` is the new and only accepting state, and every pair of inner states has a transition, using `es` wherever no transition existed in the original NFA.

---

# Problem 2: Converting a GNFA to a Regular Expression

## Algorithm Summary

The second program converts a GNFA into an equivalent regular expression by repeatedly eliminating inner states.

The algorithm preserves the new start state and the new accepting state while removing every other state one at a time. Before removing a state, the program updates the transitions between the remaining states so that every path that previously traveled through the eliminated state is still represented.

If state `k` is being removed, the transition from state `i` to state `j` is updated using:

`Rij U Rik(Rkk)*Rkj`

where:

- `Rij` represents the existing direct transition from `i` to `j`.
- `Rik` represents the transition from `i` to the state being removed.
- `Rkk` represents a loop on the state being removed.
- `Rkj` represents the transition from the removed state to `j`.
- `U` represents union.
- `*` represents Kleene star.

This repair process is repeated until only the start state and accepting state remain. The label on the transition between these two states is the regular expression recognized by the original automaton.

The major stages are:

1. Parse and validate the GNFA.
2. Select an inner state for elimination.
3. Identify incoming, outgoing, and self-loop transitions for that state.
4. Repair transitions between the remaining states.
5. Remove the selected state.
6. Repeat until only the start and accepting states remain.
7. Return the label of the final start-to-accept transition.

## Parsing the GNFA

The `GNFAParser` class in `automaton/gnfa_parser.py` converts the textual GNFA into a `GNFA` object.

Unlike an NFA transition, a GNFA transition may contain an entire regular expression. The parser therefore recognizes:

- `a`
- `b`
- `e`
- `es`
- union using `U`
- implicit concatenation
- Kleene star using `*`
- parentheses

The expression parser respects the required precedence of the operators. Kleene star has the highest precedence, concatenation is next, and union has the lowest precedence.

The first declared state is interpreted as the GNFA start state, while the final declared state is the accepting state. The states between them are the inner states that may be eliminated.

## Eliminating a State

The state-elimination process is implemented by `GNFAToRegexConverter` in `automaton/gnfa_to_regex_converter.py`.

The converter leaves the start and accepting states in the graph and repeatedly removes an inner state.

Suppose the program is eliminating state `q1`. For every remaining state `qi` that can enter `q1` and every remaining state `qj` that can be reached from `q1`, the program constructs the expression:

`Riq1(Rq1q1)*Rq1j`

This expression describes all strings that travel from `qi` into `q1`, loop at `q1` zero or more times, and then leave `q1` for `qj`.

That expression is then unioned with the existing direct transition from `qi` to `qj`.

After all affected transitions have been repaired, `q1` and its attached transitions can safely be removed without changing the language recognized by the GNFA.

## Regular-Expression Representation

The program does not store regular expressions as plain strings while performing the conversion. Instead, the `regex` package represents expressions as a tree.

`RegularExpression` provides the public operations used by the converter, including union, concatenation, and Kleene star.

Internally, expression types include:

- `SymbolNode`
- `ConcatNode`
- `UnionNode`
- `StarNode`

This design allows the program to determine when parentheses are required and to apply basic simplifications during construction.

For example:

`es U R = R`

because union with the empty set does not change a language.

Similarly:

`eR = R`

because concatenation with epsilon does not change the expression.

These simplifications prevent unnecessary components from appearing in the final regular expression.

## Worked Example

For Problem 2, the program uses the GNFA produced by Problem 1:

`q3,q0,q1,q2,q4f,q0-b->q0,q0-a->q1,q1-b->q1,q1-a->q0,q1-e->q2,q3-e->q0,q0-e->q4,q0-es->q2,q2-es->q0,q2-es->q1,q2-es->q2`

In this GNFA, `q3` is the start state and `q4` is the accepting state. The inner states `q0`, `q1`, and `q2` must be eliminated while preserving all possible paths from `q3` to `q4`.

For each eliminated state `k`, the program repairs affected transitions using:

`Rij U Rik(Rkk)*Rkj`

where `Rij` is the existing transition from `i` to `j`, `Rik` enters the state being removed, `Rkk` is its self-loop, and `Rkj` leaves the removed state.

### Eliminating q0

State `q0` has a self-loop labeled `b`. Therefore, `(R00)*` becomes:

`b*`

There is an incoming epsilon transition from `q3` to `q0`, and `q0` has outgoing transitions to `q1` and `q4`.

The path from `q3` through `q0` to `q1` becomes:

`e(b*)a`

Because concatenating with epsilon does not change a regular expression, this simplifies to:

`b*a`

Therefore, the repaired transition from `q3` to `q1` is:

`q3-b*a->q1`

There is also a path from `q3` through `q0` directly to the accepting state `q4`:

`e(b*)e`

This simplifies to:

`b*`

Therefore, the program creates:

`q3-b*->q4`

State `q1` also has a transition to `q0` labeled `a`, so eliminating `q0` produces a new path from `q1` back to itself:

`a(b*)a`

However, `q1` already has a self-loop labeled `b`. The existing and new paths are combined using union:

`b U ab*a`

Thus, after eliminating `q0`, the important remaining transitions include:

- `q3-b*a->q1`
- `q3-b*->q4`
- `q1-(bUab*a)->q1`
- `q1-ab*->q4`

The last transition results from traveling from `q1` to `q0` using `a`, looping at `q0` zero or more times using `b*`, and then following the epsilon transition from `q0` to `q4`.

### Eliminating q1

The next important inner state is `q1`.

The transition entering `q1` from `q3` is:

`b*a`

The self-loop on `q1` is:

`bUab*a`

Therefore, the loop may be repeated zero or more times:

`(bUab*a)*`

The transition from `q1` to `q4` is:

`ab*`

Combining these pieces gives the new path from `q3` through `q1` to `q4`:

`b*a(bUab*a)*ab*`

There is already a direct transition from `q3` to `q4` labeled:

`b*`

The state-elimination formula unions the existing path with the newly created path:

`b* U b*a(bUab*a)*ab*`

### Eliminating q2

State `q2` does not provide a path to the accepting state. Its outgoing transitions to the inner states are all labeled `es`, representing the empty set. Therefore, eliminating `q2` does not add any strings to the language represented by the start-to-accept transition.

After all inner states have been eliminated, only `q3` and `q4` remain. The transition between them is:

`b*Ub*a(bUab*a)*ab*`

Therefore, the regular expression returned by the program is:

**`b*Ub*a(bUab*a)*ab*`**

This is exactly the expression printed by the program when the GNFA generated in Problem 1 is supplied as input to Problem 2.

---

# AI Usage

[Describe specifically which portions of the project used AI assistance. Do not claim that AI solved either conversion problem if that did not occur. A good disclosure should identify the specific activities involved, such as assistance with documentation, debugging, unit-test ideas, code organization, or particular implementation details.]