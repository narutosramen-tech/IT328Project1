# IT328 Project 1: NFA, GNFA, and Regular Expressions

This project converts nondeterministic finite automata (NFAs) to generalized
nondeterministic finite automata (GNFAs), then converts GNFAs to equivalent
regular expressions through state elimination.

## Features

- Parse and validate NFA definitions.
- Preserve parallel NFA transitions.
- Convert NFAs to normalized GNFAs with boundary states.
- Combine parallel GNFA transitions with union.
- Parse GNFA regular-expression labels, including union, concatenation,
  Kleene star, epsilon, and the empty set.
- Convert GNFAs to regular expressions using state elimination.
- Format machine-readable automata output without spaces.

## Input format

An NFA definition lists all states first, followed by transitions. State `q0`
is the start state, and an `f` suffix marks an accepting state.

```text
q0,q1f,q0-a->q1
```

NFA transition labels are `a`, `b`, and `e`, where `e` represents epsilon.
States must be declared before their transitions.

GNFA definitions use the same general format. Their transition labels may be
regular expressions such as `aUb`, `ab`, or `(aUb)*`. The label `es` represents
the empty set.

## Output conventions

- States are rendered as `q<number>`; accepting states have an `f` suffix.
- Transitions are rendered as `q<start>-<expression>->q<end>`.
- The GNFA conversion adds a new start state and a new accepting state.
- The new start state is listed first, inner states follow, and the new
  accepting state is listed last.
- Parallel NFA transitions become one GNFA transition joined with `U`.
- Missing GNFA edges, including missing self-loops, are represented by `es`.
- Concatenation is implicit, and parentheses are added only when required by
  regular-expression precedence.

## Usage

Run the interactive program from the project root:

```bash
python main.py
```

Choose one of the available operations and enter the complete machine
definition when prompted:

1. NFA to GNFA
2. GNFA to regular expression

Conversion errors are written to standard error and cause a nonzero exit
status.

## Examples

Direct transition:

```text
Input NFA:  q0,q1f,q0-a->q1
Expected language: a
```

Parallel transitions:

```text
Input NFA:  q0,q1f,q0-a->q1,q0-b->q1
Expected direct GNFA label: aUb
Expected language: aUb
```

Loop:

```text
Input NFA:  q0,q1f,q0-a->q0,q0-e->q1
Expected language: a*
```

Concatenation:

```text
Input NFA:  q0,q1,q2f,q0-a->q1,q1-b->q2
Expected language: ab
```

No accepting path:

```text
Input NFA:  q0,q1f
Expected language: es
```

## Project structure

```text
automaton/   Automaton models, parsers, converters, and formatting
regex/       Regular-expression nodes, operations, and rendering
tests/       unittest-based unit and integration tests
main.py      Interactive command-line entry point
```

## Testing

Run the complete test suite with:

```bash
python -m unittest discover -v
```

The tests cover automaton data structures, parsing, formatting, NFA-to-GNFA
conversion, regular-expression operations, state elimination, and end-to-end
conversion behavior.
