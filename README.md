# Stack-Based Expression Evaluator

DCOMP320 Data Structures and Algorithm — Stacks Implementation (Individual Assignment, 10%)

A Python program that reads mathematical expressions from `input.txt`, evaluates each one using stacks, and writes the results to `output.txt` in the same layout as the input.

## Files

| File | Purpose |
| --- | --- |
| `stack_evaluator.py` | Main program: `Stack` class, expression evaluator, file reading/writing |
| `input.txt` | Sample input used for testing |
| `output.txt` | Output produced by running the program on `input.txt` |
| `test_stack_evaluator.py` | Unit tests (9 tests) |
| `README.md` | This file |

## Requirements

Python 3.8 or newer. No external libraries are needed.

## How to run

From the project folder:

```bash
python stack_evaluator.py
```

This reads `input.txt` and writes `output.txt`. To use other file names:

```bash
python stack_evaluator.py my_input.txt my_output.txt
```

The program also prints each expression and its result to the console.

To run the tests:

```bash
python -m unittest -v test_stack_evaluator
```

## Input file structure

One expression per line. Expressions are separated by a line containing only a separator such as `-----`.

```
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```

## Output file structure

Same layout as the input. Each expression is replaced by its result and the separator lines are copied unchanged.

```
13
-----
16
-----
-10
```

If an expression cannot be evaluated, its line shows a short error message instead, e.g. `Error: division by zero`, and the program carries on with the next expression.

## Supported syntax

- Operators: `+`, `-`, `*`, `/`
- Parentheses `( )`, including nested ones
- Standard precedence: `*` and `/` before `+` and `-`; equal levels are evaluated left to right
- Whole numbers and decimals (`7`, `2.5`, `.5`)
- Unary minus (`-5`, `3 * -2`, `-(2 + 3)`)

## Assumptions and limitations

- A separator line is 3 or more of the same symbol (`-`, `=`, `_`, `~` or `#`). The separator is copied to the output exactly.
- Blank lines are kept as blank lines.
- Whole-number results are shown without decimals (`13`, not `13.0`). Other results are rounded to at most 10 decimal places.
- `/` is true division, so `7 / 2` gives `3.5`.
- Not supported: exponents (`^`), modulo (`%`), functions (`sqrt`), variables, and implicit multiplication such as `2(3)`.
- Note on the brief: the brief's sample output shows `17` for `(8 / 4) + 7 * 2`. The correct value is `2 + 14 = 16`, which is what this program outputs.
