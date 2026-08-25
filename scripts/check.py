#!/usr/bin/env python3
"""Example helper script for the code-review skill.

Usage:
    python3 check.py <file.py>

Performs a few basic static checks and prints the results.
"""
import ast
import sys


def check(filepath: str) -> list[str]:
    findings: list[str] = []
    try:
        with open(filepath, encoding="utf-8") as f:
            source = f.read()
    except OSError as e:
        return [f"error: could not read file: {e}"]

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as e:
        return [f"error: syntax error at line {e.lineno}: {e.msg}"]

    for node in ast.walk(tree):
        # Flag use of eval()
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "eval":
                findings.append(
                    f"warning: eval() at line {node.lineno} — potential code injection"
                )
        # Flag overly broad except clauses
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(
                f"info: bare `except:` at line {node.lineno} — catch specific exceptions"
            )

    return findings or ["ok: no basic issues found"]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 check.py <file.py>")
        sys.exit(1)
    for line in check(sys.argv[1]):
        print(line)
