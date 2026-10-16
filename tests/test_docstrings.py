"""Validate that public classes and methods carry docstrings."""

import ast
from pathlib import Path


def test_all_classes_and_functions_documented() -> None:
    """Ensure the package follows the documentation requirement."""
    root = Path(__file__).resolve().parents[1] / "src/lab3package"
    missing: list[str] = []
    for file in root.glob("*.py"):
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if ast.get_docstring(node) is None:
                    missing.append(f"{file.name}:{node.lineno}:{node.name}")
    assert not missing, missing
