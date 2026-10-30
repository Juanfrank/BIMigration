#!/usr/bin/env python3
"""Pruebas de redact.py. Ejecutar: python -m unittest scripts/test_redact.py"""
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from redact import RedactingStream, redact_file, redact_text, redact_tree, redact_value  # noqa: E402


class RedactTextTests(unittest.TestCase):
    def test_m_source_host(self):
        self.assertEqual(redact_text('Origen = Sql.Databases("192.168.0.133"),'),
                         'Origen = Sql.Databases("<REDACTED:host>"),')

    def test_m_source_host_with_options(self):
        self.assertEqual(redact_text('Source = Sql.Database("srv-01", "BD")'),
                         'Source = Sql.Database("<REDACTED:host>", "BD")')

    def test_m_record_credentials(self):
        out = redact_text('Sql.Database("10.0.0.5", "BD", [UserName="sa", Password="Hunter2"])')
        self.assertNotIn("Hunter2", out)
        self.assertNotIn("10.0.0.5", out)
        self.assertIn('Password="<REDACTED>"', out)

    def test_connection_string(self):
        out = redact_text("Server=mi-sql;User ID=svc;Pwd=x;Database=D")
        self.assertEqual(out, "Server=<REDACTED:host>;User ID=<REDACTED:user>;Pwd=<REDACTED>;Database=D")

    def test_quoted_connection_host(self):
        self.assertEqual(redact_text('Server="mi-sql";Database=D'), 'Server="<REDACTED:host>";Database=D')

    def test_url_userinfo(self):
        self.assertEqual(redact_text("https://admin:s3cret@api.ejemplo.do/x"),
                         "https://<REDACTED:user>@api.ejemplo.do/x")

    def test_powerbi_endpoint(self):
        self.assertEqual(redact_text("Data Source=powerbi://api.powerbi.com/v1.0/myorg/Sales;x"),
                         "Data Source=<REDACTED:host>;x")

    def test_ip_anywhere(self):
        self.assertEqual(redact_text("conectar a 192.168.0.25 para datos"), "conectar a <REDACTED:ip> para datos")

    def test_no_false_positive_on_dax(self):
        text = "VAR _Secretarial = IF(_Secretarial, 1)"
        self.assertEqual(redact_text(text), text)


class RedactValueTests(unittest.TestCase):
    def test_sensitive_keys_replaced_whole(self):
        out = redact_value({"connectionString": "Data Source=x", "model": {"connection": "Server=10.0.0.1"},
                            "name": "ok"})
        self.assertEqual(out, {"connectionString": "<REDACTED>", "model": {"connection": "<REDACTED>"}, "name": "ok"})

    def test_empty_sensitive_value_kept(self):
        self.assertEqual(redact_value({"password": ""}), {"password": ""})

    def test_original_not_mutated(self):
        src = {"a": "10.0.0.1"}
        redact_value(src)
        self.assertEqual(src, {"a": "10.0.0.1"})


class FileTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def write(self, name, text):
        path = os.path.join(self.dir, name)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        return path

    def test_json_stays_valid(self):
        path = self.write("a.json", json.dumps({"s": 'Server=10.1.1.1;Password="x;y"'}))
        self.assertTrue(redact_file(path, json_mode=True))
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertNotIn("10.1.1.1", data["s"])

    def test_unchanged_json_not_rewritten(self):
        original = '{ "a":   1,\n  "b": "texto" }'
        path = self.write("vendor.json", original)
        self.assertFalse(redact_file(path, json_mode=True))
        with open(path, encoding="utf-8") as f:
            self.assertEqual(f.read(), original)

    def test_tree_reports_only_changed(self):
        self.write("dirty.dax", 'Sql.Databases("10.0.0.2")')
        self.write("clean.dax", "EVALUATE 1")
        self.write("image.png", "binario")
        self.assertEqual(redact_tree(self.dir), ["dirty.dax"])


class StreamTests(unittest.TestCase):
    def test_split_write_is_redacted(self):
        buf = io.StringIO()
        s = RedactingStream(buf)
        s.write("conectar a 192.168.")
        s.write("0.133 fin\n")
        s.flush()
        self.assertEqual(buf.getvalue(), "conectar a <REDACTED:ip> fin\n")


if __name__ == "__main__":
    unittest.main()
