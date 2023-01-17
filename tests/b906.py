import ast

# error if method name starts with `visit_`, the type is a valid `ast` type
# which has subfields, and contains no call to a method name containing `visit`
# anywhere in it's body


# error
def visit_For():
    ...


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
def visit_foo():
    ...


# Break has no subfields to visit, so no error
def visit_Break():
    ...


# explicitly check `visit` and `generic_visit`
# doesn't start with _visit, safe
def visit():
    ...


# doesn't start with _visit, safe
def generic_visit():
    ...


# check no crash on short name
def a():
    ...


def visit_():
    ...


# Check exceptions for ast types that only contain ADSL builtin types
# i.e. don't contain any ast.AST subnodes and therefore don't need a generic_visit
def visit_alias():
    ...


def visit_Constant():
    ...


def visit_Global():
    ...


def visit_MatchSingleton():
    ...


def visit_MatchStar():
    ...


def visit_Nonlocal():
    ...


def visit_TypeIgnore():
    ...
