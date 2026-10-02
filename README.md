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

The input format marks accepting states but has no explicit start-state marker. NFA input uses `q0` as the start state. The same convention must be made unambiguous for GNFA input.

Recommended convention: normalize every GNFA so that its new start state is `q0` and its sole accepting state is `q1f`. Original NFA states can be renumbered when necessary. If the team chooses another convention, document it and use it consistently in the formatter, GNFA parser, CLI, and tests.

## Implementation roadmap

### Phase 1: Finish the automaton model

- [ ] Decide and document the GNFA start-state convention.
- [ ] Fix `GNFA.combine_transitions()` so its early-return condition checks `len(transitions)`, not `len(self.transitions)`.
- [ ] Validate that `combine_transitions()` receives a nonempty list of transitions with matching endpoints.
- [ ] Validate constructor and method inputs where appropriate.
- [ ] Ensure copied GNFA states do not mutate the original NFA states.
- [ ] Ensure a GNFA has exactly one accepting state after conversion.
- [ ] Ensure old accepting states are no longer marked accepting.
- [ ] Ensure every required inner-state pair has exactly one transition.
- [ ] Ensure missing edges are represented by `es`, including missing self-loops.
- [ ] Ensure parallel NFA transitions are unioned into one GNFA transition.

### Phase 2: Complete NFA parsing and formatting

- [ ] Reject an empty input string and empty comma-separated tokens.
- [ ] Reject malformed state names such as `x0`, `q`, `qf`, `q1ff`, and negative numbers.
- [ ] Reject duplicate state declarations.
- [ ] Reject transitions before all referenced states have been declared.
- [ ] Reject accepting-state suffixes inside transition endpoints.
- [ ] Reject unsupported NFA labels.
- [ ] Require `q0` as the NFA start state.
- [ ] Decide whether whitespace is accepted and apply that policy consistently.
- [ ] Implement deterministic NFA formatting: states first, then transitions, no spaces, stable ordering.
- [ ] Add an NFA format/parse round-trip test.

### Phase 3: NFA-to-GNFA conversion

- [ ] Implement or complete `nfa_to_gnfa_converter.py` as the public conversion API.
- [ ] Copy states and transitions without sharing mutable state objects with the NFA.
- [ ] Add a new start state with one epsilon transition to the old start state.
- [ ] Add a new accepting state.
- [ ] Add an epsilon transition from every old accepting state to the new accepting state.
- [ ] Remove accepting status from all old accepting states.
- [ ] Combine parallel transitions using union.
- [ ] Add `es` transitions for missing inner-state pairs.
- [ ] Format the resulting GNFA using the documented state-numbering convention.
- [ ] Add conversion tests for one accepting state, multiple accepting states, an accepting start state, parallel edges, self-loops, and missing edges.

### Phase 4: GNFA regular-expression parsing

- [ ] Implement `gnfa_parser.py`.
- [ ] Parse GNFA state and transition declarations.
- [ ] Parse atomic labels: `a`, `b`, `e`, and `es`.
- [ ] Parse parenthesized expressions.
- [ ] Parse Kleene star.
- [ ] Parse implicit concatenation.
- [ ] Parse union with `U`.
- [ ] Enforce precedence: star, concatenation, union.
- [ ] Reject unmatched parentheses, repeated operators, missing operands, and invalid symbols.
- [ ] Enforce one GNFA start state and one accepting state according to the selected convention.
- [ ] Decide whether duplicate GNFA transitions are rejected or unioned, then test that policy.
- [ ] Add parser round-trip tests for every supported expression shape.

### Phase 5: State elimination

- [ ] Implement `gnfa_to_regex_converter.py`.
- [ ] Validate that the GNFA has a start state and exactly one accepting state.
- [ ] Select an elimination order excluding the start and accepting states.
- [ ] For each state `k`, update every pair `i`, `j` using:

  ```text
  Rij = Rij U Rik(Rkk)*Rkj
  ```

- [ ] Use regex operations instead of string concatenation.
- [ ] Preserve existing direct paths while adding paths through the eliminated state.
- [ ] Handle missing paths as `es`.
- [ ] Handle self-loops through `(Rkk)*`.
- [ ] Remove each eliminated state and its transitions safely.
- [ ] Stop with only the start and accepting states remaining.
- [ ] Return the start-to-accept expression, or `es` when no accepting path exists.
- [ ] Add tests for direct paths, concatenation, union, loops, epsilon paths, multiple routes, and unreachable states.

### Phase 6: Output formatting

- [ ] Complete `automaton_formatter.py`.
- [ ] Format state names as `q<number>` and append `f` only to accepting states.
- [ ] Format transitions as `q<start>-<expression>->q<end>`.
- [ ] Never insert spaces into machine-readable output.
- [ ] Use deterministic ordering for states and transitions.
- [ ] Ensure parentheses are emitted only when required by precedence.
- [ ] Ensure the final regular expression contains no spaces.
- [ ] Add exact-output tests for representative examples.

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

- [ ] State equality uses numeric names correctly.
- [ ] State formatting handles accepting and non-accepting states.
- [ ] Duplicate state names are rejected.
- [ ] Transition equality and formatting work correctly.
- [ ] Missing transition endpoints are rejected.
- [ ] Removing a state removes all connected transitions.
- [ ] Removing transitions behaves correctly for parallel edges.

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

- [ ] Parse a minimal valid NFA.
- [ ] Parse multiple accepting states.
- [ ] Parse epsilon transitions.
- [ ] Parse self-loops.
- [ ] Parse parallel transitions and preserve them separately.
- [ ] Reject malformed states and transitions.
- [ ] Reject undeclared endpoints.
- [ ] Reject missing `q0`.
- [ ] Reject duplicate declarations.

### Unit tests: GNFA conversion

- [ ] Add new start and accepting states.
- [ ] Add epsilon edge from the new start to the old start.
- [ ] Add epsilon edges from all old accepting states to the new accepting state.
- [ ] Clear old acceptance flags.
- [ ] Convert `q0-a->q1,q0-b->q1` to one `aUb` edge.
- [ ] Add `es` edges for missing transitions.
- [ ] Preserve and combine self-loops.
- [ ] Preserve the original NFA after conversion.
- [ ] Verify that GNFA output can be parsed again.

### Unit tests: GNFA parser

- [ ] Parse a normalized GNFA.
- [ ] Parse `a`, `b`, `e`, and `es` labels.
- [ ] Parse union, concatenation, star, and nested parentheses.
- [ ] Reject invalid expressions.
- [ ] Reject invalid state declarations.
- [ ] Reject invalid start/accepting-state structure.

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

- [ ] NFA string → NFA object → GNFA object.
- [ ] NFA string → GNFA output string → parsed GNFA object.
- [ ] GNFA string → regex.
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

- [ ] Decide GNFA start-state and boundary-state numbering convention.
- [ ] Decide whether whitespace is accepted in input.
- [ ] Decide whether duplicate GNFA transitions are rejected or unioned.
- [ ] Decide terminal-only CLI versus graphical/web UI.
- [ ] Define exact output ordering requirements.
- [ ] Document the complete input and output grammar.

### Core model

- [ ] Add stronger type and value validation to `State`.
- [ ] Add stronger type validation to `Transition`.
- [ ] Review `Automaton` mutation methods and error behavior.
- [ ] Fix `GNFA.combine_transitions()` guard condition.
- [ ] Add GNFA structural validation.
- [ ] Add NFA structural validation for empty and malformed machines.

### NFA parsing and conversion

- [ ] Finish NFA parser edge-case validation.
- [ ] Implement NFA formatter.
- [ ] Implement NFA-to-GNFA converter API.
- [ ] Implement boundary-state creation and numbering policy.
- [ ] Implement parallel-transition unioning.
- [ ] Implement missing-edge insertion.
- [ ] Add NFA and GNFA conversion tests.

### Regex parsing

- [ ] Design regex grammar.
- [ ] Implement tokenizer or character scanner.
- [ ] Implement parser for atomic symbols.
- [ ] Implement parser for parentheses.
- [ ] Implement parser for Kleene star.
- [ ] Implement parser for concatenation.
- [ ] Implement parser for union.
- [ ] Add malformed-regex error messages.
- [ ] Add regex parser tests.

### State elimination

- [ ] Implement elimination-order selection.
- [ ] Implement the state-elimination recurrence.
- [ ] Implement transition lookup and replacement helpers.
- [ ] Handle self-loops.
- [ ] Handle missing paths as `es`.
- [ ] Remove eliminated states safely.
- [ ] Return the final start-to-accept expression.
- [ ] Add state-elimination unit tests.

### Formatting and I/O

- [ ] Implement automaton formatter.
- [ ] Implement GNFA formatter.
- [ ] Implement final regex formatter integration.
- [ ] Guarantee no spaces in machine-readable output.
- [ ] Guarantee required parentheses only.
- [ ] Add deterministic output ordering.

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
- [ ] Add regression tests for every discovered bug.
- [ ] Run formatting and linting checks.
- [ ] Add type checking if required by the course.
- [ ] Remove debug output and temporary code.
- [ ] Review imports so the project works consistently as a package and from the CLI.
- [ ] Update this README as design decisions change.
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
