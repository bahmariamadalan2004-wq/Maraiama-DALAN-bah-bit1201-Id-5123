"""
Stack-Based Expression Evaluator
DCOMP320 Data Structures and Algorithm - Stacks Implementation

Reads mathematical expressions from input.txt, evaluates each one using
stacks (a two-stack version of Dijkstra's shunting-yard algorithm), and
writes the results to output.txt in the same layout as the input, with
each expression replaced by its result and separator lines kept as they are.

Usage:
    python stack_evaluator.py                      # input.txt -> output.txt
    python stack_evaluator.py my_in.txt my_out.txt # custom file names
"""

import re
import sys


# ---------------------------------------------------------------------------
# 1. Stack class
# ---------------------------------------------------------------------------
class StackEmptyError(Exception):
    """Raised when pop() or peek() is called on an empty stack."""


class Stack:
    """A LIFO (Last In, First Out) stack backed by a Python list.

    The top of the stack is the END of the list, so push and pop are O(1).
    """

    def __init__(self):
        self._items = []

    def push(self, item):
        """Place an item on top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item. Raises StackEmptyError if empty."""
        if self.is_empty():
            raise StackEmptyError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it. Raises StackEmptyError if empty."""
        if self.is_empty():
            raise StackEmptyError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        """Return True if the stack holds no items."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items on the stack."""
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


# ---------------------------------------------------------------------------
# 2. Expression parsing and evaluation
# ---------------------------------------------------------------------------
# Higher number = binds tighter. 'u-' is unary minus (e.g. -5 or -(2+3)).
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "u-": 3}

# A separator line is 3 or more of the same symbol, e.g. ----- or =====
SEPARATOR_PATTERN = re.compile(r"^\s*([-=_~#])\1{2,}\s*$")


def tokenize(expression):
    """Split an expression string into numbers (floats) and symbol tokens."""
    tokens = []
    i = 0
    while i < len(expression):
        ch = expression[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit() or ch == ".":
            j = i
            while j < len(expression) and (expression[j].isdigit() or expression[j] == "."):
                j += 1
            number_text = expression[i:j]
            try:
                tokens.append(float(number_text))
            except ValueError:
                raise ValueError(f"invalid number '{number_text}'")
            i = j
        elif ch in "+-*/()":
            tokens.append(ch)
            i += 1
        else:
            raise ValueError(f"invalid character '{ch}'")
    return tokens


def apply_operator(operands, operators):
    """Pop one operator and its operand(s), compute, and push the result."""
    op = operators.pop()
    try:
        if op == "u-":
            operands.push(-operands.pop())
            return
        right = operands.pop()
        left = operands.pop()
    except StackEmptyError:
        raise ValueError("malformed expression (missing operand)")

    if op == "+":
        operands.push(left + right)
    elif op == "-":
        operands.push(left - right)
    elif op == "*":
        operands.push(left * right)
    elif op == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        operands.push(left / right)


def evaluate_expression(expression):
    """Evaluate an infix expression with +, -, *, /, parentheses and precedence.

    Two stacks are used:
      operands  - holds numbers waiting to be combined
      operators - holds operators and '(' waiting to be applied
    """
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("empty expression")

    operands = Stack()
    operators = Stack()
    previous = None  # kind of the last token: 'number', 'operator', '(' or ')'

    for token in tokens:
        if isinstance(token, float):
            if previous in ("number", ")"):
                raise ValueError("missing operator between values")
            operands.push(token)
            previous = "number"

        elif token == "(":
            if previous in ("number", ")"):
                raise ValueError("missing operator before '('")
            operators.push(token)
            previous = "("

        elif token == ")":
            if previous in (None, "operator", "("):
                raise ValueError("unexpected ')'")
            # Apply everything back to the matching '('
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(operands, operators)
            if operators.is_empty():
                raise ValueError("mismatched parentheses")
            operators.pop()  # discard the '('
            previous = ")"

        else:  # + - * /
            if previous in (None, "operator", "("):
                # Operator with no left operand: allow unary minus / plus only
                if token == "-":
                    operators.push("u-")
                    previous = "operator"
                    continue
                if token == "+":
                    previous = "operator"  # unary plus changes nothing
                    continue
                raise ValueError(f"operator '{token}' is missing a left operand")
            # Precedence rule: first apply any waiting operator that binds
            # at least as tightly (gives left-to-right order for equal levels)
            while (not operators.is_empty()
                   and operators.peek() != "("
                   and PRECEDENCE[operators.peek()] >= PRECEDENCE[token]):
                apply_operator(operands, operators)
            operators.push(token)
            previous = "operator"

    if previous in ("operator", "("):
        raise ValueError("expression ends unexpectedly")

    # Apply whatever operators are left
    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("mismatched parentheses")
        apply_operator(operands, operators)

    result = operands.pop()
    if not operands.is_empty():
        raise ValueError("malformed expression")
    return result


def format_result(value):
    """Show whole numbers without '.0' (13 not 13.0); trim long decimals."""
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    return f"{value:.10f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------------------
# 3. File handling
# ---------------------------------------------------------------------------
def is_separator(line):
    """True if the line is only a separator such as ----- ."""
    return bool(SEPARATOR_PATTERN.match(line))


def process_file(input_path, output_path):
    """Read expressions, evaluate them, and write results in the same layout.

    Returns a list of (expression, result) pairs for the console summary.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    output_lines = []
    results = []
    for line in lines:
        stripped = line.strip()
        if stripped == "":
            output_lines.append("")            # keep blank lines
        elif is_separator(stripped):
            output_lines.append(stripped)      # keep the same separator
        else:
            try:
                result = format_result(evaluate_expression(stripped))
            except (ValueError, ZeroDivisionError) as error:
                result = f"Error: {error}"
            output_lines.append(result)
            results.append((stripped, result))

    # 4. Write the results file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")

    return results


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    try:
        results = process_file(input_path, output_path)
    except FileNotFoundError:
        print(f"Error: could not find '{input_path}'.")
        sys.exit(1)

    print(f"Evaluated {len(results)} expression(s) from '{input_path}':\n")
    for expression, result in results:
        print(f"  {expression:<30} => {result}")
    print(f"\nResults written to '{output_path}'.")


if __name__ == "__main__":
    main()
