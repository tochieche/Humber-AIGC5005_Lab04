
"""Test whether application classes and methods have docstrings."""

import ast
import unittest
from pathlib import Path


class TestDocstrings(unittest.TestCase):
    """Verify that classes and functions are documented."""

    def test_classes_and_functions_have_docstrings(self):
        """Check all application classes and methods."""
        root = Path(__file__).resolve().parents[1]

        files = [
            root / "main.py",
            *sorted((root / "src" / "lab3package").glob("*.py")),
        ]

        missing = []

        for file in files:
            tree = ast.parse(file.read_text(encoding="utf-8"))

            for node in ast.walk(tree):
                if isinstance(
                    node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    if ast.get_docstring(node) is None:
                        missing.append(
                            f"{file.name}: {node.name} "
                            f"(line {node.lineno})"
                        )

        self.assertEqual(
            missing,
            [],
            "Missing docstrings:\n" + "\n".join(missing),
        )


if __name__ == "__main__":
    unittest.main()
