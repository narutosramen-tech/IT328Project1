# IT328 Project 1: NFA, GNFA, and Regular Expressions

## Project goal

This project has two related programs:

1. Convert an NFA definition string into a normalized GNFA definition string.
2. Read a GNFA definition string, eliminate its states, and print an equivalent regular expression.

The program should support states named `q0`, `q1`, `q10`, and so on. State `q0` is the NFA start state. An `f` suffix marks an accepting state, for example `q2f`.

NFA transitions use the form:

```text
q<start>-<symbol>->q<end>
```

where the symbol is `a`, `b`, or `e` (`e` represents the empty string). States must be declared before transitions. For example:

```text
q0,q1f,q0-a->q1
```

The GNFA uses the same general format, but transition labels may be complete regular expressions such as `aUb`, `ab`, or `(aUb)*`. `es` represents the empty set.

## Current implementation

The following pieces already exist in some form:

- `State`, `Transition`, and the base `Automaton` classes.
- `NFA` validation and restriction of NFA labels to `a`, `b`, and `e`.
- `NFAParser` for basic NFA state and transition syntax.
- A regex expression tree supporting union with `U`, implicit concatenation, Kleene star with `*`, epsilon `e`, empty set `es`, simplification, and precedence-aware parentheses.
- `GNFA.from_nfa()` for copying an NFA, adding boundary states, transferring accepting states through epsilon transitions, adding empty-set edges, and combining parallel transitions.

For example, the NFA transitions:

```text
q0-a->q1,q0-b->q1
```

must remain two transitions in the NFA and become one GNFA transition:

```text
q0-aUb->q1
```

## Important representation decision

The input format marks accepting states but has no explicit start-state marker. NFA input uses `q0` as the start state. GNFA output therefore declares the new start state first, followed by inner states, and the sole accepting state last.

The current convention uses the first two unused nonnegative state numbers for the new start and accepting states. The serialized GNFA order—not the numeric names—identifies the boundaries. This remains pending instructor confirmation.

## Implementation roadmap

### Phase 1: Finish the automaton model

- [x] Use the first two unused nonnegative state numbers as the GNFA boundary states. This is the current convention pending instructor confirmation.
- [x] Fix `GNFA.combine_transitions()` so its early-return condition checks `len(transitions)`, not `len(self.transitions)`.
- [x] Validate that `combine_transitions()` receives a nonempty list of transitions with matching endpoints.
- [x] Validate constructor and method inputs where appropriate.
- [x] Ensure copied GNFA states do not mutate the original NFA states.
- [x] Ensure a GNFA has exactly one accepting state after conversion.
- [x] Ensure old accepting states are no longer marked accepting.
- [x] Ensure every required inner-state pair has exactly one transition.
- [x] Ensure missing edges are represented by `es`, including missing self-loops.
- [x] Ensure parallel NFA transitions are unioned into one GNFA transition.

### Phase 2: Complete NFA parsing and formatting

- [x] Reject an empty input string and empty comma-separated tokens.
- [x] Reject malformed state names such as `x0`, `q`, `qf`, `q1ff`, and negative numbers.
- [x] Reject duplicate state declarations.
- [x] Reject transitions before all referenced states have been declared.
- [x] Reject accepting-state suffixes inside transition endpoints.
- [x] Reject unsupported NFA labels.
- [x] Require `q0` as the NFA start state.
- [x] Accept and ignore whitespace throughout NFA input parsing.
- [x] Implement deterministic NFA formatting: states first, then transitions, no spaces, stable insertion ordering.
- [x] Add an NFA format/parse round-trip test.

### Phase 3: NFA-to-GNFA conversion

- [x] Implement `nfa_to_gnfa_converter.py` as the public conversion API.
- [x] Copy states and transitions without sharing mutable state objects with the NFA.
- [x] Add a new start state with one epsilon transition to the old start state.
- [x] Add a new accepting state.
- [x] Add an epsilon transition from every old accepting state to the new accepting state.
- [x] Remove accepting status from all old accepting states.
- [x] Combine parallel transitions using union.
- [x] Add `es` transitions for missing inner-state pairs.
- [x] Format the resulting GNFA using the current first-two-free-numbers convention.
- [x] Add conversion tests for boundary states, epsilon edges, parallel edges, missing edges, and preservation of the original NFA.
- [x] Add additional conversion tests for multiple accepting states, an accepting start state, and self-loops.

### Phase 4: GNFA regular-expression parsing

- [x] Implement `gnfa_parser.py`.
- [x] Parse GNFA state and transition declarations.
- [x] Parse atomic labels: `a`, `b`, `e`, and `es`.
- [x] Parse parenthesized expressions.
- [x] Parse Kleene star.
- [x] Parse implicit concatenation.
- [x] Parse union with `U`.
- [x] Enforce precedence: star, concatenation, union.
- [x] Reject unmatched parentheses, repeated operators, missing operands, and invalid symbols.
- [x] Enforce one GNFA start state and one accepting state according to the selected convention.
- [x] Reject duplicate GNFA transitions between the same ordered pair.
- [x] Add parser round-trip tests for normalized GNFA output.

### Phase 5: State elimination

- [x] Implement `gnfa_to_regex_converter.py`.
- [x] Validate that the GNFA has a start state and exactly one accepting state.
- [x] Select an elimination order excluding the start and accepting states.
- [x] For each state `k`, update every pair `i`, `j` using:

  ```text
  Rij = Rij U Rik(Rkk)*Rkj
  ```

- [x] Use regex operations instead of string concatenation.
- [x] Preserve existing direct paths while adding paths through the eliminated state.
- [x] Handle missing paths as `es`.
- [x] Handle self-loops through `(Rkk)*`.
- [x] Remove each eliminated state and its transitions safely without mutating the input GNFA.
- [x] Stop with only the start and accepting states remaining in the elimination calculation.
- [x] Return the start-to-accept expression, or `es` when no accepting path exists.
- [x] Add tests for direct paths, concatenation, loops, and unreachable states.

### Phase 6: Output formatting

- [x] Automaton formatting is implemented through NFA.__str__() and GNFA.__str__().
- [x] Format state names as `q<number>` and append `f` only to accepting states.
- [x] Format transitions as `q<start>-<expression>->q<end>`.
- [x] Never insert spaces into machine-readable output.
- [x] Use deterministic insertion ordering for states and transitions.
- [x] Ensure parentheses are emitted only when required by precedence.
- [x] Ensure the final regular expression contains no spaces.
- [x] Add exact-output tests for representative NFA and regex examples.

### Phase 7: CLI/UI

- [ ] Create one executable entry point, such as `main.py` or `__main__.py`.
- [ ] Provide `nfa-to-gnfa` mode.
- [ ] Provide `gnfa-to-regex` mode.
- [ ] Optionally provide a combined mode for NFA input directly to a regex.
- [ ] Support input from a command-line argument.
- [ ] Support standard input for long definitions.
- [ ] Optionally support `--input-file` and `--output-file`.
- [ ] Print only the requested machine-readable result to standard output.
- [ ] Print human-readable errors to standard error.
- [ ] Return a nonzero exit code for invalid input or conversion failures.
- [ ] Add `--help` with syntax examples.
- [ ] Add optional `--verbose` or `--debug` output without contaminating normal output.
- [ ] Decide whether a graphical/web UI is required. A terminal CLI is sufficient unless the assignment specifically requires a graphical UI.
- [ ] Add end-to-end CLI tests.

## Test plan

### Unit tests: data structures

- [x] State equality uses numeric names correctly.
- [x] State formatting handles accepting and non-accepting states.
- [x] Duplicate state names are rejected.
- [x] Transition equality and formatting work correctly.
- [x] Missing transition endpoints are rejected.
- [x] Removing a state removes all connected transitions.
- [x] Removing transitions behaves correctly for parallel edges.

### Unit tests: regex operations

- [x] Factory methods for `a`, `b`, `e`, and `es`.
- [x] Union simplification.
- [x] Concatenation simplification.
- [x] Kleene-star simplification.
- [x] Precedence-aware parentheses.
- [x] Equality behavior.
- [ ] Parsing and formatting round trips.
- [ ] More complex nested expressions.
- [ ] Verify that simplification preserves the represented language.

### Unit tests: NFA parser

- [x] Parse a minimal valid NFA.
- [x] Parse multiple accepting states.
- [x] Parse epsilon transitions.
- [x] Parse self-loops.
- [x] Parse parallel transitions and preserve them separately.
- [x] Reject malformed states and transitions.
- [x] Reject undeclared endpoints.
- [x] Reject missing `q0`.
- [x] Reject duplicate declarations.

### Unit tests: GNFA conversion

- [x] Add new start and accepting states.
- [x] Add epsilon edge from the new start to the old start.
- [x] Add epsilon edges from all old accepting states to the new accepting state.
- [x] Clear old acceptance flags.
- [x] Convert `q0-a->q1,q0-b->q1` to one `aUb` edge.
- [x] Add `es` edges for missing transitions.
- [x] Preserve and combine self-loops, including deduplication of nested union alternatives.
- [x] Preserve the original NFA after conversion.
- [x] Verify that GNFA output can be parsed again.

### Unit tests: GNFA parser

- [x] Parse a normalized GNFA.
- [x] Parse `a`, `b`, `e`, and `es` labels.
- [x] Parse union, concatenation, star, and nested parentheses.
- [x] Reject invalid expressions.
- [x] Reject invalid state declarations.
- [x] Reject invalid start/accepting-state structure.

### Unit tests: state elimination

- [ ] Direct single-symbol path.
- [ ] Direct epsilon path.
- [ ] Two paths requiring union.
- [ ] Two sequential edges requiring concatenation.
- [ ] A loop requiring Kleene star.
- [ ] A loop combined with an incoming and outgoing path.
- [ ] Multiple intermediate states.
- [ ] Unreachable states.
- [ ] No accepting path, producing `es`.
- [ ] A language accepting the empty string.
- [ ] Compare results against known expressions or language simulations.

### Integration and CLI tests

- [x] NFA string → NFA object → GNFA object.
- [ ] NFA string → GNFA output string → parsed GNFA object.
- [x] GNFA string → regex.
- [ ] NFA string → GNFA string → regex.
- [ ] Invalid input produces a useful error and nonzero exit code.
- [ ] Standard input works.
- [ ] File input works if implemented.
- [ ] Normal output contains no diagnostic text or spaces.
- [ ] `--help` works.

## Suggested example cases

### Direct transition

```text
Input NFA:  q0,q1f,q0-a->q1
Expected language: a
```

### Parallel transitions

```text
Input NFA:  q0,q1f,q0-a->q1,q0-b->q1
Expected direct GNFA label: aUb
Expected language: aUb
```

### Loop

```text
Input NFA:  q0,q1f,q0-a->q0,q0-e->q1
Expected language: a*
```

### Concatenation

```text
Input NFA:  q0,q1,q2f,q0-a->q1,q1-b->q2
Expected language: ab
```

### No accepting path

```text
Input NFA:  q0,q1f
Expected language: es
```

## Kanban backlog

The following issues are intended to be copied into the team Kanban board.

### Planning and design

- [x] Establish the current GNFA boundary-state numbering convention: use the first two free numbers, pending instructor confirmation.
- [x] Decide to accept and ignore whitespace in input.
- [x] Decide to reject duplicate GNFA transitions between the same ordered pair.
- [ ] Decide terminal-only CLI versus graphical/web UI.
- [x] Define current output ordering: new start first, inner states next, new accepting state last, followed by transitions.
- [ ] Document the complete input and output grammar.

### Core model

- [x] Add stronger type and value validation to `State`.
- [x] Add stronger type validation to `Transition`.
- [x] Review `Automaton` mutation methods and error behavior.
- [x] Fix `GNFA.combine_transitions()` guard condition.
- [x] Add GNFA structural validation.
- [x] Add NFA structural validation for empty and malformed machines.

### NFA parsing and conversion

- [x] Finish NFA parser edge-case validation.
- [x] Implement NFA string formatting.
- [x] Implement NFA-to-GNFA converter API.
- [x] Implement boundary-state creation and the current numbering policy.
- [x] Implement parallel-transition unioning.
- [x] Implement missing-edge insertion.
- [x] Add NFA and GNFA conversion tests.

### Regex parsing

- [x] Design regex grammar.
- [x] Implement a character-scanning recursive-descent parser.
- [x] Implement parser for atomic symbols.
- [x] Implement parser for parentheses.
- [x] Implement parser for Kleene star.
- [x] Implement parser for concatenation.
- [x] Implement parser for union.
- [x] Add malformed-regex error messages.
- [x] Add regex parser tests.

### State elimination

- [x] Implement elimination-order selection.
- [x] Implement the state-elimination recurrence.
- [x] Implement transition lookup and replacement helpers.
- [x] Handle self-loops.
- [x] Handle missing paths as `es`.
- [x] Remove eliminated states safely.
- [x] Return the final start-to-accept expression.
- [x] Add state-elimination unit tests.

### Formatting and I/O

- [x] Automaton formatting is implemented through NFA.__str__() and GNFA.__str__().
- [x] Implement GNFA string formatting with boundary states in normalized order.
- [ ] Implement final regex formatter integration.
- [x] Guarantee no spaces in machine-readable automaton output.
- [x] Guarantee required parentheses only for the existing regex AST.
- [x] Add deterministic insertion ordering.

### CLI/UI

- [ ] Add application entry point.
- [ ] Add `nfa-to-gnfa` command.
- [ ] Add `gnfa-to-regex` command.
- [ ] Add optional combined command.
- [ ] Add standard-input support.
- [ ] Add file-input support.
- [ ] Add file-output support if needed.
- [ ] Add help text and examples.
- [ ] Add human-readable error handling.
- [ ] Add exit-code handling.
- [ ] Add optional verbose/debug mode.
- [ ] Add CLI integration tests.

### Quality and delivery

- [ ] Add tests for every public class and method.
- [ ] Add end-to-end tests.
- [x] Add regression tests for discovered NFA/GNFA bugs.
- [ ] Run formatting and linting checks.
- [ ] Add type checking if required by the course.
- [ ] Remove debug output and temporary code.
- [x] Review test imports so public classes are imported from the package API.
- [x] Update this README as design decisions change.
- [ ] Add final usage examples.
- [ ] Verify the project from a clean checkout.

## Definition of done

The project is complete when:

- A valid NFA string can be parsed reliably.
- Parallel NFA transitions are preserved in the NFA and unioned in the GNFA.
- The GNFA has the required new start and accepting states.
- Missing GNFA edges are represented by `es`.
- A GNFA string can be parsed, including complex regular-expression labels.
- State elimination produces an equivalent regular expression.
- Output has the required syntax, ordering, spacing, and parentheses.
- Invalid input produces useful errors.
- Both program modes work from the CLI.
- Unit, integration, and CLI tests pass.
