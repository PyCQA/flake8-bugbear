import ast

import libcst
import libcst as cst
from libcst import CSTTransformer
from libcst import CSTVisitor as Visitor

# error if method name starts with `visit_`, the type is a valid `ast` type
# which has subfields, and contains no call to a method name containing `visit`
# anywhere in it's body


# error
def visit_For(): ... # B906: 0


# has call to visit function
def visit_For():
    foo_visit_bar()


# has call to visit method
def visit_While():
    foo.bar_visit_bar()


# this visit call clearly won't run, but is treated as safe
def visit_If():
    def foo():
        a_visit_function()


# not a valid AST class, no error
def visit_foo(): ...


# Break has no subfields to visit, so no error
def visit_Break(): ...


# explicitly check `visit` and `generic_visit`
# doesn't start with _visit, safe
def visit(): ...


# doesn't start with _visit, safe
def generic_visit(): ...


# check no crash on short name
def a(): ...


def visit_(): ...


# Check exceptions for ast types that only contain ADSL builtin types
# i.e. don't contain any ast.AST subnodes and therefore don't need a generic_visit
def visit_alias(): ...


def visit_Constant(): ...


def visit_Global(): ...


def visit_MatchSingleton(): ...


def visit_MatchStar(): ...


def visit_Nonlocal(): ...


def visit_TypeIgnore(): ...


# These nodes are deprecated, but some codebases may still use them
# for backwards-compatibility with Python 3.7
def visit_Bytes(): ...


def visit_Num(): ...


def visit_Str(): ...


# methods of ast visitors are checked
class AstVisitor(ast.NodeVisitor):
    def visit_For(self, node): ...  # B906: 4


# a base we can't resolve might be an ast visitor, so it's still checked
class SubVisitor(AstVisitor):
    def visit_For(self, node): ...  # B906: 4


# libcst visitors have no generic_visit and visit children automatically
class LibcstVisitor(libcst.CSTVisitor):
    def visit_ClassDef(self, node): ...


class AliasedLibcstVisitor(cst.CSTVisitor):
    def visit_For(self, node): ...


class ImportedLibcstTransformer(CSTTransformer):
    def visit_If(self, node): ...


class ImportedAliasedLibcstVisitor(Visitor):
    def visit_While(self, node): ...
