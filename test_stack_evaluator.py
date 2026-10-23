"""Unit tests for stack_evaluator.py. Run with: python -m unittest -v"""
import os
import tempfile
import unittest

from stack_evaluator import Stack, StackEmptyError, evaluate_expression, format_result, process_file


class TestStack(unittest.TestCase):
    def test_push_pop_peek(self):
        s = Stack()
        s.push(1); s.push(2); s.push(3)
        self.assertEqual(s.peek(), 3)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.size(), 1)

    def test_empty_stack_errors(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        with self.assertRaises(StackEmptyError):
            s.pop()
        with self.assertRaises(StackEmptyError):
            s.peek()


class TestEvaluate(unittest.TestCase):
    def check(self, expr, expected):
        self.assertAlmostEqual(evaluate_expression(expr), expected)

    def test_brief_examples(self):
        self.check("3 + 5 * 2", 13)
        self.check("(8 / 4) + 7 * 2", 16)
        self.check("10 - (2 + 3) * 4", -10)

    def test_precedence_and_associativity(self):
        self.check("2 + 3 * 4 - 1", 13)
        self.check("100 - 20 - 30", 50)
        self.check("64 / 4 / 2", 8)

    def test_parentheses(self):
        self.check("((2 + 3) * (4 - 1)) / 5", 3)

    def test_unary_minus_and_decimals(self):
        self.check("-5 + 3 * (-2)", -11)
        self.check("1.5 * 4", 6)

    def test_errors(self):
        for bad in ["8 / 0", "(3 + 4", "3 + 4)", "5 + * 2", "2 3", "abc", ""]:
            with self.assertRaises((ValueError, ZeroDivisionError)):
                evaluate_expression(bad)

    def test_format(self):
        self.assertEqual(format_result(13.0), "13")
        self.assertEqual(format_result(3.5), "3.5")


class TestFiles(unittest.TestCase):
    def test_same_layout(self):
        with tempfile.TemporaryDirectory() as d:
            inp, out = os.path.join(d, "in.txt"), os.path.join(d, "out.txt")
            with open(inp, "w") as f:
                f.write("3 + 5 * 2\n-----\n10 - (2 + 3) * 4\n")
            process_file(inp, out)
            with open(out) as f:
                self.assertEqual(f.read(), "13\n-----\n-10\n")


if __name__ == "__main__":
    unittest.main()
