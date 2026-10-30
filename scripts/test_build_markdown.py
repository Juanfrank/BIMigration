#!/usr/bin/env python3
"""Pruebas del criterio del Apéndice B de build_markdown.py. Ejecutar: python -m unittest scripts/test_build_markdown.py"""
import importlib.util
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location("build_markdown", os.path.join(HERE, "build_markdown.py"))
bm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bm)

REL = {"from_table": "Ventas", "from_column": "IdCliente", "to_table": "Clientes", "to_column": "IdCliente"}


def model(*measures):
    return {"measures": [{"table": t, "name": n, "expression": e} for t, n, e in measures]}


class ActivationTests(unittest.TestCase):
    def test_qualified_call_activates(self):
        m = model(("T", "M", "CALCULATE([x], USERELATIONSHIP(Ventas[IdCliente], Clientes[IdCliente]))"))
        self.assertEqual(bm.relationship_activation(REL, m, {("T", "M")}), ["T[M]"])

    def test_reversed_arguments_activate(self):
        m = model(("T", "M", "CALCULATE([x], USERELATIONSHIP(Clientes[IdCliente], Ventas[IdCliente]))"))
        self.assertEqual(bm.relationship_activation(REL, m, {("T", "M")}), ["T[M]"])

    def test_same_column_name_other_table_does_not_activate(self):
        m = model(("T", "M", "CALCULATE([x], USERELATIONSHIP(Pagos[IdCliente], Clientes[IdCliente]))"))
        self.assertEqual(bm.relationship_activation(REL, m, {("T", "M")}), [])

    def test_measure_outside_closure_ignored(self):
        m = model(("T", "M", "CALCULATE([x], USERELATIONSHIP(Ventas[IdCliente], Clientes[IdCliente]))"))
        self.assertEqual(bm.relationship_activation(REL, m, set()), [])

    def test_quoted_table_names(self):
        m = model(("T", "M", "CALCULATE([x], USERELATIONSHIP('Ventas'[IdCliente], 'Clientes'[IdCliente]))"))
        self.assertEqual(bm.relationship_activation(REL, m, {("T", "M")}), ["T[M]"])

    def test_no_userelationship_no_activation(self):
        m = model(("T", "M", "SUM(Ventas[IdCliente])"))
        self.assertEqual(bm.relationship_activation(REL, m, {("T", "M")}), [])


class ClosureTests(unittest.TestCase):
    def test_dependencies_are_followed(self):
        m = model(("T", "A", "[B] + 1"), ("T", "B", "[C]"), ("T", "C", "1"), ("T", "Z", "2"))
        self.assertEqual(bm.page_measure_closure({("T", "A")}, m), {("T", "A"), ("T", "B"), ("T", "C")})


class AppendixTests(unittest.TestCase):
    def test_both_sides_in_page_included_others_excluded(self):
        mdl = {"measures": [], "relationships": [
            dict(REL, name="ambas", from_cardinality="many", to_cardinality="one", from_cardinality_is_default=True,
                 to_cardinality_is_default=True, cross_filtering_behavior="oneDirection", is_active=True),
            dict(REL, name="una", from_table="Ventas", to_table="Otra", from_cardinality="many", to_cardinality="one",
                 from_cardinality_is_default=True, to_cardinality_is_default=True,
                 cross_filtering_behavior="oneDirection", is_active=True)]}
        rows = bm.build_appendix_b({"Ventas", "Clientes"}, mdl, set())
        self.assertEqual([r[0] for r in rows], ["ambas"])


if __name__ == "__main__":
    unittest.main()
