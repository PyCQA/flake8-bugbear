import ast

import libcst as cst

# Dict unpacking has no value expression on Python 3.15.
unpacked = {**d for d in dicts}


class LibcstVisitor(cst.CSTVisitor):
    def visit_Call(self, node): ...


class Outer:
    unpacked = {**d for d in dicts}

    class LibcstVisitor(cst.CSTVisitor):
        def visit_Call(self, node): ...


class AstVisitor(ast.NodeVisitor):
    def visit_Call(self, node): ...  # B906: 4
