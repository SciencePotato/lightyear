import ast
import os
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


SOURCE = Path(__file__).resolve().parents[1] / "emailValidity/emailValidity.py"


class ExportTests(unittest.TestCase):
    def test_save_uses_a_string_clean_filename_for_multi_dot_input(self):
        tree = ast.parse(SOURCE.read_text())
        definition = next(node for node in tree.body if isinstance(node, ast.ClassDef))
        check = next(node for node in definition.body if isinstance(node, ast.FunctionDef) and node.name == "check")
        namespace = {"os": os}
        exec(compile(ast.Module(body=[check], type_ignores=[]), str(SOURCE), "exec"), namespace)
        for inplace, expected in [
            (False, "../flask/uploadFolder/contacts.export_clean.csv"),
            (True, "../flask/uploadFolder/contacts.export.csv"),
        ]:
            frame = SimpleNamespace(to_csv=Mock())
            instance = SimpleNamespace(multi=False, filename="/synthetic/contacts.export.csv",
                                       df=frame, checkTheMail=Mock())
            self.assertIs(namespace["check"](instance, save=True, inplace=inplace), frame)
            instance.checkTheMail.assert_called_once_with()
            frame.to_csv.assert_called_once_with(expected, index=False)


if __name__ == "__main__":
    unittest.main()
