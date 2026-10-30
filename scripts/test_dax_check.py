#!/usr/bin/env python3
"""Pruebas de dax_check.py. Ejecutar: python -m unittest scripts/test_dax_check.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dax_check import check_expression  # noqa: E402


class DetectsProblemsTests(unittest.TestCase):
    def assertProblem(self, expr):
        self.assertTrue(check_expression(expr), f"debía detectar un problema en: {expr!r}")

    def test_unclosed_parenthesis(self):
        self.assertProblem("CALCULATE([x], T[c]")

    def test_unclosed_string(self):
        self.assertProblem('IF(T[u] = "abc, 1, 0)')

    def test_stray_block_close(self):
        self.assertProblem("VAR a = 1 */ RETURN a")

    def test_unclosed_block_comment(self):
        self.assertProblem("VAR a = 1 /* sin cerrar")

    def test_trailing_comma(self):
        self.assertProblem("CALCULATE([x], T[c],)")

    def test_trailing_operator(self):
        self.assertProblem("VAR a = 1 +")


class AcceptsValidTests(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(check_expression("CALCULATE([x], T[c])"), [])

    def test_comments_removed_cleanly(self):
        self.assertEqual(check_expression("VAR a = 1 // nota\nRETURN a /* b */"), [])

    def test_markers_inside_strings_are_code(self):
        self.assertEqual(check_expression('IF(T[u]="http://x -- y",1,0)'), [])

    def test_nested_comment_block_is_valid(self):
        self.assertEqual(check_expression("A /* x /* y */ z */ B"), [])


if __name__ == "__main__":
    unittest.main()
