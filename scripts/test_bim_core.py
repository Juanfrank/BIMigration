#!/usr/bin/env python3
"""Pruebas de parse_m_source (bim_core.py). Ejecutar: python -m unittest scripts/test_bim_core.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bim_core import extract_refs, parse_m_source, strip_dax_comments  # noqa: E402


class NavigationTests(unittest.TestCase):
    def test_schema_and_item(self):
        r = parse_m_source('let O = Sql.Databases("h"), D = O{[Name="D"]}[Data], T = D{[Schema="dbo",Item="vwA"]}[Data] in T')
        self.assertEqual(r, {"kind": "navigation",
                             "objects": [{"database": "D", "schema": "dbo", "name": "vwA"}]})


class NativeQueryTests(unittest.TestCase):
    def test_from_join_and_three_part_names(self):
        expr = 'let O = Sql.Database("h","db",[Query="SELECT x FROM [dbo].[T1] JOIN base.penal.T2 b ON 1=1"]) in O'
        r = parse_m_source(expr)
        self.assertEqual(r["kind"], "native_query")
        self.assertEqual(r["objects"], [{"database": "db", "schema": "dbo", "name": "T1"},
                                        {"database": "base", "schema": "penal", "name": "T2"}])

    def test_comments_do_not_hide_query(self):
        expr = 'let O = Sql.Database("h","db",[Query="-- nota#(lf)SELECT x FROM dbo.T1#(lf)/* FROM falso */"]) in O'
        self.assertEqual(parse_m_source(expr)["objects"], [{"database": "db", "schema": "dbo", "name": "T1"}])

    def test_cte_names_are_not_sources(self):
        expr = 'let O = Sql.Database("h","db",[Query="WITH C AS (SELECT 1 a) SELECT * FROM C JOIN dbo.T1 t ON 1=1"]) in O'
        self.assertEqual(parse_m_source(expr)["objects"], [{"database": "db", "schema": "dbo", "name": "T1"}])

    def test_sql_in_variable(self):
        expr = ('let Origen = Sql.Databases("h"), BD = Origen{[Name="Depo"]}[Data], '
                'SQL = "SELECT a FROM dbo.Salas AS s" in Value.NativeQuery(BD, SQL, null)')
        self.assertEqual(parse_m_source(expr)["objects"], [{"database": "Depo", "schema": "dbo", "name": "Salas"}])

    def test_query_text_never_returned(self):
        expr = 'let O = Sql.Database("h","db",[Query="SELECT secreto FROM dbo.T1"]) in O'
        self.assertNotIn("secreto", repr(parse_m_source(expr)))


class OtherKindsTests(unittest.TestCase):
    def test_reference_to_model_table(self):
        self.assertEqual(parse_m_source("let Origen = vwSGJProductos in Origen"),
                         {"kind": "reference", "objects": [{"database": None, "schema": None, "name": "vwSGJProductos"}]})
        self.assertEqual(parse_m_source("let Source = dvwUsuariosBO, X = Table.SelectColumns(Source,{})  in X")["kind"],
                         "reference")

    def test_file_origin_has_no_path(self):
        r = parse_m_source('let S = SharePoint.Files("https://x.sharepoint.com/sites/a/b.xlsx") in S')
        self.assertEqual(r, {"kind": "file", "objects": []})
        self.assertNotIn("sharepoint", repr(r).lower())

    def test_embedded_data(self):
        self.assertEqual(parse_m_source('let S = Table.FromRows(Json.Document("x")) in S')["kind"], "embedded")

    def test_empty_or_unknown(self):
        self.assertEqual(parse_m_source(None), {"kind": None, "objects": []})
        self.assertEqual(parse_m_source("VAR x = 1 RETURN x")["kind"], None)


class ExtractRefsTests(unittest.TestCase):
    def test_refs_ignore_strings_and_comments(self):
        obj = {"kind": "measure", "expression": 'VAR a = "[no]" // [tampoco]\nRETURN CALCULATE([M], T[C])'}
        self.assertEqual(set(extract_refs(obj)), {(None, "M"), ("T", "C")})


class StripCommentsTests(unittest.TestCase):
    def test_line_comments(self):
        self.assertEqual(strip_dax_comments("VAR a = 1 // nota\nRETURN a"), "VAR a = 1\nRETURN a")
        self.assertEqual(strip_dax_comments("x = 1 -- nota\n+ 2"), "x = 1\n+ 2")

    def test_block_comment_across_lines(self):
        self.assertEqual(strip_dax_comments("CALCULATE(\n /* quitar\n esto */ SUM(T[c]) )"),
                         "CALCULATE(\n   SUM(T[c]) )")

    def test_markers_inside_strings_are_kept(self):
        self.assertEqual(strip_dax_comments('IF(T[u] = "http://x -- y", 1, 0) // fin'),
                         'IF(T[u] = "http://x -- y", 1, 0)')

    def test_markers_inside_identifiers_are_kept(self):
        self.assertEqual(strip_dax_comments("SUM('a//b'[c]) -- z"), "SUM('a//b'[c])")
        self.assertEqual(strip_dax_comments("SUM(T[a//b]) // z"), "SUM(T[a//b])")

    def test_nested_block_comments(self):
        self.assertEqual(strip_dax_comments("A /* x /*y*/ z */ B"), "A   B")

    def test_comment_only_expression_is_empty(self):
        self.assertEqual(strip_dax_comments("// solo comentario"), "")

    def test_blank_lines_collapse(self):
        self.assertEqual(strip_dax_comments("A\n\n// x\n\n\nB"), "A\n\nB")


if __name__ == "__main__":
    unittest.main()
