# AI contribution guidelines

These conventions apply to AI-assisted changes in this project. Follow them
for new code, edits, tests, and documentation unless a more specific user
request overrides them.

## Project context

This is a Python project for converting NFAs to GNFAs and converting GNFAs to
regular expressions. The main packages are:

- `automaton/`: states, transitions, NFAs, GNFAs, parsers, converters, and formatters.
- `regex/`: regular-expression nodes, operations, and rendering.
- `tests/`: `unittest` test modules.

## General editing rules

- Inspect the relevant files before changing them.
- Preserve existing user changes and do not overwrite unrelated work.
- Make the smallest change that fully satisfies the request.
- Use `apply_patch` for local file edits.
- Do not use destructive commands such as `git reset --hard` or `git checkout --` unless explicitly requested.
- Do not create generated files, caches, or build artifacts in the repository.
- Do not add dependencies without documenting the reason and updating the project configuration if one exists.
- Keep public behavior compatible unless the task explicitly requires a behavior change.
- Report validation limitations honestly, especially when Python or a test runner is unavailable.

## Python formatting

- Use four spaces for indentation.
- Use one class or function definition per logical block with normal blank-line separation.
- Keep the existing project style for multiline definitions:

  ```python
  def method(
          self,
          value: str
      ) -> str:
      """..."""
  ```

- Put the return annotation on every function and method.
- Use type annotations for parameters, attributes, and return values.
- Use the built-in generic forms already used by the project, such as `list[State]` and `tuple[int, bool]`.
- Keep imports at the top of the file and remove unused imports introduced by a change.
- Keep lines readable; avoid dense one-line implementations when they reduce clarity.
- Preserve the project’s existing line-ending and formatting behavior when possible.
- Run `git diff --check` after editing.

## Classes and methods

- Use `PascalCase` for classes and `snake_case` for methods, functions, attributes, and local variables.
- Use `UPPER_SNAKE_CASE` for module-level constants.
- Keep constructors focused on initializing object state.
- Validate inputs at public boundaries and raise `ValueError` for invalid values or structure.
- Raise `TypeError` when an argument has the wrong type.
- Use `NotImplementedError` for abstract method bodies; never use `raise NotImplemented`.
- Preserve equality and hashing consistency. If `__eq__` compares a field, `__hash__` must use compatible identity semantics.
- Keep `__str__()` as the canonical default human-readable representation.
- Put optional formatting behavior in an explicit method such as `to_string(...)`, rather than adding formatting arguments to `__str__()`.
- Use `__repr__()` for developer-oriented, unambiguous representations that expose the object structure.

## Comments and docstrings

- Add a class docstring describing the class’s purpose and important attributes.
- Add a docstring to every public method and function.
- Use the existing Google-style sections:
  - `Args:` for parameters;
  - `Raises:` for exceptions;
  - `Returns:` for return values.
- Document defaults for optional parameters.
- Explain why non-obvious logic exists, especially GNFA normalization and state elimination.
- Prefer comments that explain intent, invariants, or algorithmic decisions over comments that repeat the code.
- Keep comments accurate when behavior changes.
- Do not claim that a method validates or preserves something unless the implementation actually does so.
- Use the project’s existing author header when adding a new Python source or test file:

  ```python
  """
  Authors: Jon Bailey, Thomas Hrycenko, and Tolu Olatunbosun

  All code was written by students and all comments were written by AI.
  """
  ```

## Automaton conventions

- States use numeric names and render as `q<number>`.
- Accepting states render with an `f` suffix, such as `q2f`.
- NFA input uses `q0` as the start state.
- NFA transitions may be labeled only `a`, `b`, or `e`.
- NFA parallel transitions remain separate.
- GNFA parallel transitions between the same ordered pair are combined with union, such as `aUb`.
- GNFA missing edges use the empty-set expression `es`.
- Machine-readable automaton output lists all states before all transitions.
- Machine-readable automaton output uses commas as separators and contains no spaces.
- Transition endpoints do not include the accepting marker; acceptance belongs to state declarations.
- Preserve insertion order unless the task specifically requires deterministic sorting. If output ordering must be stable across construction paths, implement and document an explicit ordering policy.

## Regular-expression conventions

- Use `RegularExpression` operations instead of manually concatenating regex strings during algorithms.
- Use `union()`, `concatenate()`, and `kleene_star()` so simplification and precedence-aware parentheses remain centralized.
- Use `e` for epsilon and `es` for the empty set.
- Use uppercase `U` for union.
- Concatenation is implicit.
- Parenthesize only when required by precedence.
- Keep regex AST node `__repr__()` methods recursive and constructor-like.

## Test conventions

- Use `unittest`, matching the existing tests.
- Test modules must start with `test_`, for example:
  - `tests/test_nfa.py`
  - `tests/test_nfa_parser.py`
  - `tests/test_regular_expressions.py`
- Do not use names ending in `_test.py` for new test modules.
- Test classes should inherit from `unittest.TestCase` and use names beginning with `Test`.
- Test methods must begin with `test_` and test one behavior or closely related behavior.
- Use the project’s multiline function-definition style and add a docstring to each test method.
- Include both valid cases and invalid-input cases.
- Test observable behavior rather than private implementation details unless the private behavior is itself an explicit requirement.
- Include exact string-output assertions for parsers and formatters.
- Include tests for:
  - empty and malformed input;
  - duplicate states;
  - undeclared transition endpoints;
  - epsilon transitions;
  - self-loops;
  - parallel transitions;
  - accepting states;
  - missing transitions and `es` edges;
  - regex precedence and parentheses;
  - round-trip formatting and parsing;
  - end-to-end NFA → GNFA → regex behavior.
- Prefer small test fixtures or helper methods for repeated setup.
- Do not make tests depend on unordered collection behavior.

## Validation workflow

After a code change:

1. Inspect the diff.
2. Run `git diff --check`.
3. Run the relevant test module.
4. Run the complete test suite with `python -m unittest discover -v` when Python is available.
5. Check that generated output has the required syntax, ordering, commas, spacing, and parentheses.
6. Report which checks passed and which could not be run.

When adding a feature, add tests in the same change whenever practical. When
fixing a bug, add a regression test that would have failed before the fix.

## CLI and output rules

- Keep machine-readable results on standard output.
- Send human-readable diagnostics to standard error.
- Return a nonzero exit code for invalid input or conversion failures.
- Keep normal output free of debug messages and extra spaces.
- Add help text and examples for new CLI modes or options.

## Documentation rules

- Update `README.md` when implementation behavior, input grammar, output grammar, CLI usage, or project status changes.
- Keep the README roadmap and Kanban backlog synchronized with completed work.
- Do not mark a task complete merely because a stub or placeholder exists.
