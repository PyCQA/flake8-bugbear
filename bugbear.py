from __future__ import annotations

import ast
import builtins
import itertools
import logging
import math
import re
import sys
import warnings
from collections import Counter, defaultdict, namedtuple
from contextlib import suppress
from functools import lru_cache, partial
from keyword import iskeyword
from typing import Dict, Iterable, Iterator, List, Sequence, Set, Union

import attr
import pycodestyle  # type: ignore[import-untyped]

__version__ = "24.12.12"

LOG = logging.getLogger("flake8.bugbear")
CONTEXTFUL_NODES = (
    ast.Module,
    ast.ClassDef,
    ast.AsyncFunctionDef,
    ast.FunctionDef,
    ast.Lambda,
    ast.ListComp,
    ast.SetComp,
    ast.DictComp,
    ast.GeneratorExp,
)
FUNCTION_NODES = (ast.AsyncFunctionDef, ast.FunctionDef, ast.Lambda)
B908_pytest_functions = {"raises", "warns"}
B908_unittest_methods = {
    "assertRaises",
    "assertRaisesRegex",
    "assertRaisesRegexp",
    "assertWarns",
    "assertWarnsRegex",
}

B902_default_decorators = {"classmethod"}

Context = namedtuple("Context", ["node", "stack"])


@attr.s(unsafe_hash=False)
class BugBearChecker:
    name = "flake8-bugbear"
    version = __version__

    tree = attr.ib(default=None)
    filename = attr.ib(default="(none)")
    lines = attr.ib(default=None)
    max_line_length = attr.ib(default=79)
    visitor = attr.ib(init=False, factory=lambda: BugBearVisitor)
    options = attr.ib(default=None)

    def run(self):
        if not self.tree or not self.lines:
            self.load_file()

        if self.options and hasattr(self.options, "extend_immutable_calls"):
            b008_b039_extend_immutable_calls = set(self.options.extend_immutable_calls)
        else:
            b008_b039_extend_immutable_calls = set()

        b902_classmethod_decorators: set[str] = B902_default_decorators
        if self.options and hasattr(self.options, "classmethod_decorators"):
            b902_classmethod_decorators = set(self.options.classmethod_decorators)

        visitor = self.visitor(
            filename=self.filename,
            lines=self.lines,
            b008_b039_extend_immutable_calls=b008_b039_extend_immutable_calls,
            b902_classmethod_decorators=b902_classmethod_decorators,
        )
        visitor.visit(self.tree)
        for e in itertools.chain(visitor.errors, self.gen_line_based_checks()):
            if self.should_warn(e.message[:4]):
                yield self.adapt_error(e)

    def gen_line_based_checks(self):
        """gen_line_based_checks() -> (error, error, error, ...)

        The following simple checks are based on the raw lines, not the AST.
        """
        noqa_type_ignore_regex = re.compile(
            r"#\s*(noqa|type:\s*ignore|pragma:)[^#\r\n]*$"
        )
        for lineno, line in enumerate(self.lines, start=1):
            # Special case: ignore long shebang (following pycodestyle).
            if lineno == 1 and line.startswith("#!"):
                continue

            # At first, removing noqa and type: ignore trailing comments"
            no_comment_line = noqa_type_ignore_regex.sub("", line)
            if no_comment_line != line:
                no_comment_line = noqa_type_ignore_regex.sub("", no_comment_line)

            length = len(no_comment_line) - 1
            if length > 1.1 * self.max_line_length and no_comment_line.strip():
                # Special case long URLS and paths to follow pycodestyle.
                # Would use the `pycodestyle.maximum_line_length` directly but
                # need to supply it arguments that are not available so chose
                # to replicate instead.
                chunks = no_comment_line.split()

                is_line_comment_url_path = len(chunks) == 2 and chunks[0] == "#"

                just_long_url_path = len(chunks) == 1

                num_leading_whitespaces = len(no_comment_line) - len(chunks[-1])
                too_many_leading_white_spaces = (
                    num_leading_whitespaces >= self.max_line_length - 7
                )

                skip = is_line_comment_url_path or just_long_url_path
                if skip and not too_many_leading_white_spaces:
                    continue

                yield B950(lineno, length, vars=(length, self.max_line_length))

    @classmethod
    def adapt_error(cls, e):
        """Adapts the extended error namedtuple to be compatible with Flake8."""
        return e._replace(message=e.message.format(*e.vars))[:4]

    def load_file(self) -> None:
        """Loads the file in a way that auto-detects source encoding and deals
        with broken terminal encodings for stdin.

        Stolen from flake8_import_order because it's good.
        """

        if self.filename in ("stdin", "-", None):
            self.filename = "stdin"
            self.lines = pycodestyle.stdin_get_value().splitlines(True)
        else:
            self.lines = pycodestyle.readlines(self.filename)

        if not self.tree:
            self.tree = ast.parse("".join(self.lines))

    @staticmethod
    def add_options(optmanager) -> None:
        """Informs flake8 to ignore B9xx by default."""
        optmanager.extend_default_ignore(disabled_by_default)
        optmanager.add_option(
            "--extend-immutable-calls",
            comma_separated_list=True,
            parse_from_config=True,
            default=[],
            help="Skip B008 test for additional immutable calls.",
        )
        # you cannot register the same option in two different plugins, so we
        # only register --classmethod-decorators if pep8-naming is not installed
        if "pep8ext_naming" not in sys.modules.keys():
            optmanager.add_option(
                "--classmethod-decorators",
                comma_separated_list=True,
                parse_from_config=True,
                default=B902_default_decorators,
                help=(
                    "List of method decorators that should be treated as classmethods"
                    " by B902"
                ),
            )

    @lru_cache  # noqa: B019
    def should_warn(self, code) -> bool:
        """Returns `True` if Bugbear should emit a particular warning.

        flake8 overrides default ignores when the user specifies
        `ignore = ` in configuration.  This is problematic because it means
        specifying anything in `ignore = ` implicitly enables all optional
        warnings.  This function is a workaround for this behavior.

        As documented in the README, the user is expected to explicitly select
        the warnings.

        NOTE: This method is deprecated and will be removed in a future release. It is
        recommended to use `extend-ignore` and `extend-select` in your flake8
        configuration to avoid implicitly altering selected and ignored codes.
        """
        if code[:2] != "B9":
            # Normal warnings are safe for emission.
            return True

        if self.options is None:
            # Without options configured, Bugbear will emit B9 but flake8 will ignore
            LOG.info(
                "Options not provided to Bugbear, optional warning %s selected.", code
            )
            return True

        for i in range(2, len(code) + 1):
            if self.options.select and code[:i] in self.options.select:
                return True

            # flake8 >=4.0: Also check for codes in extend_select
            if (
                hasattr(self.options, "extend_select")
                and self.options.extend_select
                and code[:i] in self.options.extend_select
            ):
                return True

        LOG.info(
            "Optional warning %s not present in selected warnings: %r. Not "
            "firing it at all.",
            code,
            self.options.select,
        )
        return False


def _is_identifier(arg) -> bool:
    # Return True if arg is a valid identifier, per
    # https://docs.python.org/2/reference/lexical_analysis.html#identifiers

    if not isinstance(arg, ast.Constant) or not isinstance(arg.value, str):
        return False

    return re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", arg.value) is not None


def _flatten_excepthandler(node: ast.expr | None) -> Iterator[ast.expr | None]:
    if not isinstance(node, ast.Tuple):
        yield node
        return
    expr_list = node.elts.copy()
    while len(expr_list):
        expr = expr_list.pop(0)
        if isinstance(expr, ast.Starred) and isinstance(
            expr.value, (ast.List, ast.Tuple)
        ):
            expr_list.extend(expr.value.elts)
            continue

        yield expr


def _check_redundant_excepthandlers(names: Sequence[str], node, in_trystar):
    # See if any of the given exception names could be removed, e.g. from:
    #    (MyError, MyError)  # duplicate names
    #    (MyError, BaseException)  # everything derives from the Base
    #    (Exception, TypeError)  # builtins where one subclasses another
    #    (IOError, OSError)  # IOError is an alias of OSError since Python3.3
    # but note that other cases are impractical to handle from the AST.
    # We expect this is mostly useful for users who do not have the
    # builtin exception hierarchy memorised, and include a 'shadowed'
    # subtype without realising that it's redundant.
    good = sorted(set(names), key=names.index)
    if "BaseException" in good:
        good = ["BaseException"]
    # Remove redundant exceptions that the automatic system either handles
    # poorly (usually aliases) or can't be checked (e.g. it's not an
    # built-in exception).
    for primary, equivalents in B014_REDUNDANT_EXCEPTIONS.items():
        if primary in good:
            good = [g for g in good if g not in equivalents]

    for name, other in itertools.permutations(tuple(good), 2):
        if _typesafe_issubclass(
            getattr(builtins, name, type), getattr(builtins, other, ())
        ):
            if name in good:
                good.remove(name)
    if good != names:
        desc = good[0] if len(good) == 1 else "({})".format(", ".join(good))
        as_ = " as " + node.name if node.name is not None else ""
        return B014(
            node.lineno,
            node.col_offset,
            vars=(", ".join(names), as_, desc, in_trystar),
        )
    return None


def _to_name_str(node):
    # Turn Name and Attribute nodes to strings, e.g "ValueError" or
    # "pkg.mod.error", handling any depth of attribute accesses.
    # Return None for unrecognized nodes.
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Call):
        return _to_name_str(node.func)
    elif isinstance(node, ast.Attribute):
        inner = _to_name_str(node.value)
        if inner is None:
            return None
        return f"{inner}.{node.attr}"
    else:
        return None


def names_from_assignments(assign_target):
    if isinstance(assign_target, ast.Name):
        yield assign_target.id
    elif isinstance(assign_target, ast.Starred):
        yield from names_from_assignments(assign_target.value)
    elif isinstance(assign_target, (ast.List, ast.Tuple)):
        for child in assign_target.elts:
            yield from names_from_assignments(child)


def children_in_scope(node):
    yield node
    if not isinstance(node, FUNCTION_NODES):
        for child in ast.iter_child_nodes(node):
            yield from children_in_scope(child)


def walk_list(nodes):
    for node in nodes:
        yield from ast.walk(node)


def _typesafe_issubclass(cls, class_or_tuple):
    try:
        return issubclass(cls, class_or_tuple)
    except TypeError:
        # User code specifies a type that is not a type in our current run. Might be
        # their error, might be a difference in our environments. We don't know so we
        # ignore this
        return False


class ExceptBaseExceptionVisitor(ast.NodeVisitor):
    def __init__(self, except_node: ast.ExceptHandler) -> None:
        super().__init__()
        self.root = except_node
        self._re_raised = False

    def re_raised(self) -> bool:
        self.visit(self.root)
        return self._re_raised

    def visit_Raise(self, node: ast.Raise):
        """If we find a corresponding `raise` or `raise e` where e was from
        `except BaseException as e:` then we mark re_raised as True and can
        stop scanning."""
        if node.exc is None or (
            isinstance(node.exc, ast.Name) and node.exc.id == self.root.name
        ):
            self._re_raised = True
            return
        return super().generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node is not self.root:
            return  # entered a nested except - stop searching
        return super().generic_visit(node)


@attr.define
class B040CaughtException:
    name: str
    has_note: bool


class B041UnhandledKeyType:
    """
    A dictionary key of a type that we do not check for duplicates.
    """


@attr.define(frozen=True)
class B041VariableKeyType:
    name: str


@attr.s
class BugBearVisitor(ast.NodeVisitor):
    filename = attr.ib()
    lines = attr.ib()
    b008_b039_extend_immutable_calls: set[str] = attr.ib(factory=set)
    b902_classmethod_decorators: set[str] = attr.ib(factory=set)
    node_window: list[ast.AST] = attr.ib(factory=list)
    errors: list[error] = attr.ib(factory=list)
    contexts: list[Context] = attr.ib(factory=list)
    b040_caught_exception: B040CaughtException | None = attr.ib(default=None)

    NODE_WINDOW_SIZE = 4
    _b023_seen: set[error] = attr.ib(factory=set, init=False)
    _b005_imports: set[str] = attr.ib(factory=set, init=False)

    # set to "*" when inside a try/except*, for correctly printing errors
    in_trystar: str = attr.ib(default="")

    if False:
        # Useful for tracing what the hell is going on.

        def __getattr__(self, name: str):
            print(name)
            return self.__getattribute__(name)

    @property
    def node_stack(self):
        if len(self.contexts) == 0:
            return []

        context, stack = self.contexts[-1]
        return stack

    def in_class_init(self) -> bool:
        return (
            len(self.contexts) >= 2
            and isinstance(self.contexts[-2].node, ast.ClassDef)
            and isinstance(self.contexts[-1].node, ast.FunctionDef)
            and self.contexts[-1].node.name == "__init__"
        )

    def visit_Return(self, node: ast.Return) -> None:
        if self.in_class_init():
            if node.value is not None:
                self.errors.append(B037(node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_Yield(self, node: ast.Yield) -> None:
        if self.in_class_init():
            self.errors.append(B037(node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_YieldFrom(self, node: ast.YieldFrom) -> None:
        if self.in_class_init():
            self.errors.append(B037(node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit(self, node) -> None:
        is_contextful = isinstance(node, CONTEXTFUL_NODES)

        if is_contextful:
            context = Context(node, [])
            self.contexts.append(context)

        self.node_stack.append(node)
        self.node_window.append(node)
        self.node_window = self.node_window[-self.NODE_WINDOW_SIZE :]
        super().visit(node)
        self.node_stack.pop()

        if is_contextful:
            self.contexts.pop()

        self.check_for_b018(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.type is None:
            self.errors.append(B001(node.lineno, node.col_offset))
            self.generic_visit(node)
            return

        old_b040_caught_exception = self.b040_caught_exception
        if node.name is None:
            self.b040_caught_exception = None
        else:
            self.b040_caught_exception = B040CaughtException(node.name, False)

        names = self.check_for_b013_b014_b029_b030(node)

        if (
            "BaseException" in names
            and not ExceptBaseExceptionVisitor(node).re_raised()
        ):
            self.errors.append(B036(node.lineno, node.col_offset))

        self.generic_visit(node)

        if (
            self.b040_caught_exception is not None
            and self.b040_caught_exception.has_note
        ):
            self.errors.append(B040(node.lineno, node.col_offset))
        self.b040_caught_exception = old_b040_caught_exception

    def visit_UAdd(self, node) -> None:
        trailing_nodes = list(map(type, self.node_window[-4:]))
        if trailing_nodes == [ast.UnaryOp, ast.UAdd, ast.UnaryOp, ast.UAdd]:
            originator = self.node_window[-4]
            self.errors.append(B002(originator.lineno, originator.col_offset))
        self.generic_visit(node)

    def visit_Call(self, node) -> None:
        is_b040_add_note = False
        if isinstance(node.func, ast.Attribute):
            self.check_for_b005(node)
            is_b040_add_note = self.check_for_b040_add_note(node.func)
        else:
            with suppress(AttributeError, IndexError):
                if (
                    node.func.id in ("getattr", "hasattr")
                    and node.args[1].value == "__call__"
                ):
                    self.errors.append(B004(node.lineno, node.col_offset))
                if (
                    node.func.id == "getattr"
                    and len(node.args) == 2
                    and _is_identifier(node.args[1])
                    and not iskeyword(node.args[1].value)
                ):
                    self.errors.append(B009(node.lineno, node.col_offset))
                elif (
                    not any(isinstance(n, ast.Lambda) for n in self.node_stack)
                    and node.func.id == "setattr"
                    and len(node.args) == 3
                    and _is_identifier(node.args[1])
                    and not iskeyword(node.args[1].value)
                ):
                    self.errors.append(B010(node.lineno, node.col_offset))

        self.check_for_b026(node)
        self.check_for_b028(node)
        self.check_for_b034(node)
        self.check_for_b039(node)
        self.check_for_b905(node)
        self.check_for_b910(node)
        self.check_for_b911(node)

        # no need for copying, if used in nested calls it will be set to None
        current_b040_caught_exception = self.b040_caught_exception
        if not is_b040_add_note:
            self.check_for_b040_usage(node.args)
            self.check_for_b040_usage(node.keywords)

        self.generic_visit(node)

        if is_b040_add_note:
            # Avoid nested calls within the parameter list using the variable itself.
            # e.g. `e.add_note(str(e))`
            self.b040_caught_exception = current_b040_caught_exception

    def visit_Module(self, node) -> None:
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        self.check_for_b040_usage(node.value)
        if len(node.targets) == 1:
            t = node.targets[0]

            if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name):
                if (t.value.id, t.attr) == ("os", "environ"):
                    self.errors.append(B003(node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_For(self, node) -> None:
        self.check_for_b007(node)
        self.check_for_b020(node)
        self.check_for_b023(node)
        self.check_for_b031(node)
        self.check_for_b909(node)
        self.generic_visit(node)

    def visit_AsyncFor(self, node) -> None:
        self.check_for_b023(node)
        self.generic_visit(node)

    def visit_While(self, node) -> None:
        self.check_for_b023(node)
        self.generic_visit(node)

    def visit_ListComp(self, node) -> None:
        self.check_for_b023(node)
        self.generic_visit(node)

    def visit_SetComp(self, node) -> None:
        self.check_for_b023(node)
        self.generic_visit(node)

    def visit_DictComp(self, node) -> None:
        self.check_for_b023(node)
        self.check_for_b035(node)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node) -> None:
        self.check_for_b023(node)
        self.generic_visit(node)

    def visit_Assert(self, node) -> None:
        self.check_for_b011(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node) -> None:
        self.check_for_b902(node)
        self.check_for_b006_and_b008(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node) -> None:
        self.check_for_b901(node)
        self.check_for_b902(node)
        self.check_for_b006_and_b008(node)
        self.check_for_b019(node)
        self.check_for_b021(node)
        self.check_for_b906(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.check_for_b903(node)
        self.check_for_b021(node)
        self.check_for_b024_and_b027(node)
        self.generic_visit(node)

    def visit_Try(self, node) -> None:
        self.check_for_b012(node)
        self.check_for_b025(node)
        self.generic_visit(node)

    def visit_TryStar(self, node) -> None:
        outer_trystar = self.in_trystar
        self.in_trystar = "*"
        self.visit_Try(node)
        self.in_trystar = outer_trystar

    def visit_Compare(self, node) -> None:
        self.check_for_b015(node)
        self.generic_visit(node)

    def visit_Raise(self, node: ast.Raise) -> None:
        if node.exc is None:
            self.b040_caught_exception = None
        else:
            self.check_for_b040_usage(node.exc)
            self.check_for_b040_usage(node.cause)
        self.check_for_b016(node)
        self.check_for_b904(node)
        self.generic_visit(node)

    def visit_With(self, node) -> None:
        self.check_for_b017(node)
        self.check_for_b022(node)
        self.check_for_b908(node)
        self.generic_visit(node)

    def visit_JoinedStr(self, node) -> None:
        self.check_for_b907(node)
        self.generic_visit(node)

    def visit_AnnAssign(self, node) -> None:
        self.check_for_b032(node)
        self.check_for_b040_usage(node.value)
        self.generic_visit(node)

    def visit_Import(self, node) -> None:
        self.check_for_b005(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node) -> None:
        self.visit_Import(node)

    def visit_Set(self, node) -> None:
        self.check_for_b033(node)
        self.generic_visit(node)

    def visit_Dict(self, node) -> None:
        self.check_for_b041(node)
        self.generic_visit(node)

    def check_for_b041(self, node) -> None:
        # Complain if there are duplicate key-value pairs in a dictionary literal.
        def convert_to_value(item):
            if isinstance(item, ast.Constant):
                return item.value
            elif isinstance(item, ast.Tuple):
                return tuple(convert_to_value(i) for i in item.elts)
            elif isinstance(item, ast.Name):
                return B041VariableKeyType(item.id)
            else:
                return B041UnhandledKeyType()

        keys = [convert_to_value(key) for key in node.keys]
        key_counts = Counter(keys)
        duplicate_keys = [key for key, count in key_counts.items() if count > 1]
        for key in duplicate_keys:
            key_indices = [i for i, i_key in enumerate(keys) if i_key == key]
            seen = set()
            for index in key_indices:
                value = convert_to_value(node.values[index])
                if value in seen:
                    key_node = node.keys[index]
                    self.errors.append(B041(key_node.lineno, key_node.col_offset))
                seen.add(value)

    def check_for_b005(self, node) -> None:
        if isinstance(node, ast.Import):
            for name in node.names:
                self._b005_imports.add(name.asname or name.name)
        elif isinstance(node, ast.ImportFrom):
            for name in node.names:
                self._b005_imports.add(f"{node.module}.{name.name or name.asname}")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr not in B005_METHODS:
                return  # method name doesn't match

            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id in self._b005_imports
            ):
                return  # method is being run on an imported module

            if (
                len(node.args) != 1
                or not isinstance(node.args[0], ast.Constant)
                or not isinstance(node.args[0].value, str)
            ):
                return  # used arguments don't match the builtin strip

            value = node.args[0].value
            if len(value) == 1:
                return  # stripping just one character

            if len(value) == len(set(value)):
                return  # no characters appear more than once

            self.errors.append(B005(node.lineno, node.col_offset))

    def check_for_b006_and_b008(self, node) -> None:
        visitor = FunctionDefDefaultsVisitor(
            B006, B008, self.b008_b039_extend_immutable_calls
        )
        visitor.visit(node.args.defaults + node.args.kw_defaults)
        self.errors.extend(visitor.errors)

    def check_for_b039(self, node: ast.Call) -> None:
        if not (
            (isinstance(node.func, ast.Name) and node.func.id == "ContextVar")
            or (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "ContextVar"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "contextvars"
            )
        ):
            return
        # ContextVar only takes one kw currently, but better safe than sorry
        for kw in node.keywords:
            if kw.arg == "default":
                break
        else:
            return

        visitor = FunctionDefDefaultsVisitor(
            B039, B039, self.b008_b039_extend_immutable_calls
        )
        visitor.visit(kw.value)
        self.errors.extend(visitor.errors)

    def check_for_b007(self, node) -> None:
        targets = NameFinder()
        targets.visit(node.target)
        ctrl_names = set(filter(lambda s: not s.startswith("_"), targets.names))
        body = NameFinder()
        for expr in node.body:
            body.visit(expr)
        used_names = set(body.names)
        for name in sorted(ctrl_names - used_names):
            n = targets.names[name][0]
            self.errors.append(B007(n.lineno, n.col_offset, vars=(name,)))

    def check_for_b011(self, node) -> None:
        if isinstance(node.test, ast.Constant) and node.test.value is False:
            self.errors.append(B011(node.lineno, node.col_offset))

    def check_for_b012(self, node) -> None:
        def _loop(node, bad_node_types) -> None:
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                return

            if isinstance(node, (ast.While, ast.For)):
                bad_node_types = (ast.Return,)

            elif isinstance(node, bad_node_types):
                self.errors.append(
                    B012(node.lineno, node.col_offset, vars=(self.in_trystar,))
                )

            for child in ast.iter_child_nodes(node):
                _loop(child, bad_node_types)

        for child in node.finalbody:
            _loop(child, (ast.Return, ast.Continue, ast.Break))

    def check_for_b013_b014_b029_b030(self, node: ast.ExceptHandler) -> list[str]:
        handlers: Iterable[ast.expr | None] = _flatten_excepthandler(node.type)
        names: list[str] = []
        bad_handlers: list[object] = []
        ignored_handlers: list[ast.Name | ast.Attribute | ast.Call | ast.Starred] = []

        for handler in handlers:
            if isinstance(handler, (ast.Name, ast.Attribute)):
                name = _to_name_str(handler)
                if name is None:
                    ignored_handlers.append(handler)
                else:
                    names.append(name)
            elif isinstance(handler, (ast.Call, ast.Starred)):
                ignored_handlers.append(handler)
            else:
                bad_handlers.append(handler)
        if bad_handlers:
            self.errors.append(B030(node.lineno, node.col_offset))
        if len(names) == 0 and not bad_handlers and not ignored_handlers:
            self.errors.append(
                B029(node.lineno, node.col_offset, vars=(self.in_trystar,))
            )
        elif (
            len(names) == 1
            and not bad_handlers
            and not ignored_handlers
            and isinstance(node.type, ast.Tuple)
        ):
            self.errors.append(
                B013(
                    node.lineno,
                    node.col_offset,
                    vars=(
                        *names,
                        self.in_trystar,
                    ),
                )
            )
        else:
            maybe_error = _check_redundant_excepthandlers(names, node, self.in_trystar)
            if maybe_error is not None:
                self.errors.append(maybe_error)
        return names

    def check_for_b015(self, node) -> None:
        if isinstance(self.node_stack[-2], ast.Expr):
            self.errors.append(B015(node.lineno, node.col_offset))

    def check_for_b016(self, node) -> None:
        if isinstance(node.exc, ast.JoinedStr) or (
            isinstance(node.exc, ast.Constant)
            and (
                isinstance(node.exc.value, (int, float, complex, str, bool))
                or node.exc.value is None
            )
        ):
            self.errors.append(B016(node.lineno, node.col_offset))

    def check_for_b017(self, node) -> None:
        """Checks for use of the evil syntax 'with assertRaises(Exception):'
        or 'with pytest.raises(Exception)'.

        This form of assertRaises will catch everything that subclasses
        Exception, which happens to be the vast majority of Python internal
        errors, including the ones raised when a non-existing method/function
        is called, or a function is called with an invalid dictionary key
        lookup.
        """
        item = node.items[0]
        item_context = item.context_expr

        if (
            hasattr(item_context, "func")
            and (
                (
                    isinstance(item_context.func, ast.Attribute)
                    and (
                        item_context.func.attr == "assertRaises"
                        or (
                            item_context.func.attr == "raises"
                            and isinstance(item_context.func.value, ast.Name)
                            and item_context.func.value.id == "pytest"
                            and "match"
                            not in (kwd.arg for kwd in item_context.keywords)
                        )
                    )
                )
                or (
                    isinstance(item_context.func, ast.Name)
                    and item_context.func.id == "raises"
                    and isinstance(item_context.func.ctx, ast.Load)
                    and "pytest.raises" in self._b005_imports
                    and "match" not in (kwd.arg for kwd in item_context.keywords)
                )
            )
            and len(item_context.args) == 1
            and isinstance(item_context.args[0], ast.Name)
            and item_context.args[0].id in {"Exception", "BaseException"}
            and not item.optional_vars
        ):
            self.errors.append(B017(node.lineno, node.col_offset))

    def check_for_b019(self, node) -> None:
        if (
            len(node.decorator_list) == 0
            or len(self.contexts) < 2
            or not isinstance(self.contexts[-2].node, ast.ClassDef)
        ):
            return

        # Preserve decorator order so we can get the lineno from the decorator node
        # rather than the function node (this location definition changes in Python 3.8)
        resolved_decorators = (
            ".".join(compose_call_path(decorator)) for decorator in node.decorator_list
        )
        for idx, decorator in enumerate(resolved_decorators):
            if decorator in {"classmethod", "staticmethod"}:
                return

            if decorator in B019_CACHES:
                self.errors.append(
                    B019(
                        node.decorator_list[idx].lineno,
                        node.decorator_list[idx].col_offset,
                    )
                )
                return

    def check_for_b020(self, node) -> None:
        targets = NameFinder()
        targets.visit(node.target)
        ctrl_names = set(targets.names)

        iterset = B020NameFinder()
        iterset.visit(node.iter)
        iterset_names = set(iterset.names)

        for name in sorted(ctrl_names):
            if name in iterset_names:
                n = targets.names[name][0]
                self.errors.append(B020(n.lineno, n.col_offset, vars=(name,)))

    def check_for_b023(self, loop_node) -> None:  # noqa: C901
        """Check that functions (including lambdas) do not use loop variables.

        https://docs.python-guide.org/writing/gotchas/#late-binding-closures from
        functions - usually but not always lambdas - defined inside a loop are a
        classic source of bugs.

        For each use of a variable inside a function defined inside a loop, we
        emit a warning if that variable is reassigned on each loop iteration
        (outside the function).  This includes but is not limited to explicit
        loop variables like the `x` in `for x in range(3):`.
        """
        # Because most loops don't contain functions, it's most efficient to
        # implement this "backwards": first we find all the candidate variable
        # uses, and then if there are any we check for assignment of those names
        # inside the loop body.
        safe_functions = []
        suspicious_variables = []
        for node in ast.walk(loop_node):
            # check if function is immediately consumed to avoid false alarm
            if isinstance(node, ast.Call):
                # check for filter&reduce
                if (
                    isinstance(node.func, ast.Name)
                    and node.func.id in ("filter", "reduce", "map")
                ) or (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "reduce"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "functools"
                ):
                    for arg in node.args:
                        if isinstance(arg, FUNCTION_NODES):
                            safe_functions.append(arg)

                # check for key=
                for keyword in node.keywords:
                    if keyword.arg == "key" and isinstance(
                        keyword.value, FUNCTION_NODES
                    ):
                        safe_functions.append(keyword.value)

            # mark `return lambda: x` as safe
            # does not (currently) check inner lambdas in a returned expression
            # e.g. `return (lambda: x, )
            if isinstance(node, ast.Return):
                if isinstance(node.value, FUNCTION_NODES):
                    safe_functions.append(node.value)

            # find unsafe functions
            if isinstance(node, FUNCTION_NODES) and node not in safe_functions:
                argnames = {
                    arg.arg for arg in ast.walk(node.args) if isinstance(arg, ast.arg)
                }
                if isinstance(node, ast.Lambda):
                    body_nodes = ast.walk(node.body)
                else:
                    body_nodes = itertools.chain.from_iterable(map(ast.walk, node.body))
                errors = []
                for name in body_nodes:
                    if isinstance(name, ast.Name) and name.id not in argnames:
                        if isinstance(name.ctx, ast.Load):
                            errors.append(
                                B023(name.lineno, name.col_offset, vars=(name.id,))
                            )
                        elif isinstance(name.ctx, ast.Store):
                            argnames.add(name.id)
                for err in errors:
                    if err.vars[0] not in argnames and err not in self._b023_seen:
                        self._b023_seen.add(err)  # dedupe across nested loops
                        suspicious_variables.append(err)

        if suspicious_variables:
            reassigned_in_loop = set(self._get_assigned_names(loop_node))

        for err in sorted(suspicious_variables):
            if reassigned_in_loop.issuperset(err.vars):
                self.errors.append(err)

    def check_for_b024_and_b027(self, node: ast.ClassDef) -> None:  # noqa: C901
        """Check for inheritance from abstract classes in abc and lack of
        any methods decorated with abstract*"""

        def is_abc_class(value, name: str = "ABC"):
            # class foo(metaclass = [abc.]ABCMeta)
            if isinstance(value, ast.keyword):
                return value.arg == "metaclass" and is_abc_class(value.value, "ABCMeta")
            # class foo(ABC)
            # class foo(abc.ABC)
            return (isinstance(value, ast.Name) and value.id == name) or (
                isinstance(value, ast.Attribute)
                and value.attr == name
                and isinstance(value.value, ast.Name)
                and value.value.id == "abc"
            )

        def is_abstract_decorator(expr):
            return (isinstance(expr, ast.Name) and expr.id[:8] == "abstract") or (
                isinstance(expr, ast.Attribute) and expr.attr[:8] == "abstract"
            )

        def is_overload(expr):
            return (isinstance(expr, ast.Name) and expr.id == "overload") or (
                isinstance(expr, ast.Attribute) and expr.attr == "overload"
            )

        def empty_body(body) -> bool:
            def is_str_or_ellipsis(node):
                return isinstance(node, ast.Constant) and (
                    node.value is Ellipsis or isinstance(node.value, str)
                )

            # Function body consist solely of `pass`, `...`, and/or (doc)string literals
            return all(
                isinstance(stmt, ast.Pass)
                or (isinstance(stmt, ast.Expr) and is_str_or_ellipsis(stmt.value))
                for stmt in body
            )

        # don't check multiple inheritance
        # https://github.com/PyCQA/flake8-bugbear/issues/277
        if len(node.bases) + len(node.keywords) > 1:
            return

        # only check abstract classes
        if not any(map(is_abc_class, (*node.bases, *node.keywords))):
            return

        has_method = False
        has_abstract_method = False

        for stmt in node.body:
            # https://github.com/PyCQA/flake8-bugbear/issues/293
            # Ignore abc's that declares a class attribute that must be set
            if isinstance(stmt, ast.AnnAssign) and stmt.value is None:
                has_abstract_method = True
                continue

            # only check function defs
            if not isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            has_method = True

            has_abstract_decorator = any(
                map(is_abstract_decorator, stmt.decorator_list)
            )

            has_abstract_method |= has_abstract_decorator

            if (
                not has_abstract_decorator
                and empty_body(stmt.body)
                and not any(map(is_overload, stmt.decorator_list))
            ):
                self.errors.append(
                    B027(stmt.lineno, stmt.col_offset, vars=(stmt.name,))
                )

        if has_method and not has_abstract_method:
            self.errors.append(B024(node.lineno, node.col_offset, vars=(node.name,)))

    def check_for_b026(self, call: ast.Call) -> None:
        if not call.keywords:
            return

        starreds = [arg for arg in call.args if isinstance(arg, ast.Starred)]
        if not starreds:
            return

        first_keyword = call.keywords[0].value
        for starred in starreds:
            if (starred.lineno, starred.col_offset) > (
                first_keyword.lineno,
                first_keyword.col_offset,
            ):
                self.errors.append(B026(starred.lineno, starred.col_offset))

    def check_for_b031(self, loop_node) -> None:  # noqa: C901
        """Check that `itertools.groupby` isn't iterated over more than once.

        We emit a warning when the generator returned by `groupby()` is used
        more than once inside a loop body or when it's used in a nested loop.
        """
        # for <loop_node.target> in <loop_node.iter>: ...
        if isinstance(loop_node.iter, ast.Call):
            node = loop_node.iter
            if (isinstance(node.func, ast.Name) and node.func.id in ("groupby",)) or (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "groupby"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "itertools"
            ):
                # We have an invocation of groupby which is a simple unpacking
                if isinstance(loop_node.target, ast.Tuple) and isinstance(
                    loop_node.target.elts[1], ast.Name
                ):
                    group_name = loop_node.target.elts[1].id
                else:
                    # Ignore any `groupby()` invocation that isn't unpacked
                    return

                num_usages = 0
                for node in walk_list(loop_node.body):
                    # Handled nested loops
                    if isinstance(node, ast.For):
                        for nested_node in walk_list(node.body):
                            assert nested_node != node
                            if (
                                isinstance(nested_node, ast.Name)
                                and nested_node.id == group_name
                            ):
                                self.errors.append(
                                    B031(
                                        nested_node.lineno,
                                        nested_node.col_offset,
                                        vars=(nested_node.id,),
                                    )
                                )

                    # Handle multiple uses
                    if isinstance(node, ast.Name) and node.id == group_name:
                        num_usages += 1
                        if num_usages > 1:
                            self.errors.append(
                                B031(node.lineno, node.col_offset, vars=(node.id,))
                            )

    def _get_names_from_tuple(self, node: ast.Tuple):
        for dim in node.elts:
            if isinstance(dim, ast.Name):
                yield dim.id
            elif isinstance(dim, ast.Tuple):
                yield from self._get_names_from_tuple(dim)

    def _get_dict_comp_loop_and_named_expr_var_names(self, node: ast.DictComp):
        finder = NamedExprFinder()
        for gen in node.generators:
            if isinstance(gen.target, ast.Name):
                yield gen.target.id
            elif isinstance(gen.target, ast.Tuple):
                yield from self._get_names_from_tuple(gen.target)

            finder.visit(gen.ifs)

        yield from finder.names.keys()

    def check_for_b035(self, node: ast.DictComp) -> None:
        """Check that a static key isn't used in a dict comprehension.

        Emit a warning if a likely unchanging key is used - either a constant,
        or a variable that isn't coming from the generator expression.
        """
        if isinstance(node.key, ast.Constant):
            self.errors.append(
                B035(node.key.lineno, node.key.col_offset, vars=(node.key.value,))
            )
        elif isinstance(node.key, ast.Name):
            if node.key.id not in self._get_dict_comp_loop_and_named_expr_var_names(
                node
            ):
                self.errors.append(
                    B035(node.key.lineno, node.key.col_offset, vars=(node.key.id,))
                )

    def check_for_b040_add_note(self, node: ast.Attribute) -> bool:
        if (
            node.attr == "add_note"
            and isinstance(node.value, ast.Name)
            and self.b040_caught_exception
            and node.value.id == self.b040_caught_exception.name
        ):
            self.b040_caught_exception.has_note = True
            return True
        return False

    def check_for_b040_usage(self, node: ast.expr | None) -> None:
        def superwalk(node: ast.AST | list[ast.AST]):
            if isinstance(node, list):
                for n in node:
                    yield from ast.walk(n)
            else:
                yield from ast.walk(node)

        if not self.b040_caught_exception or node is None:
            return

        for n in superwalk(node):
            if isinstance(n, ast.Name) and n.id == self.b040_caught_exception.name:
                self.b040_caught_exception = None
                break

    def _get_assigned_names(self, loop_node):
        loop_targets = (ast.For, ast.AsyncFor, ast.comprehension)
        for node in children_in_scope(loop_node):
            if isinstance(node, (ast.Assign)):
                for child in node.targets:
                    yield from names_from_assignments(child)
            if isinstance(node, loop_targets + (ast.AnnAssign, ast.AugAssign)):
                yield from names_from_assignments(node.target)

    def check_for_b904(self, node) -> None:
        """Checks `raise` without `from` inside an `except` clause.

        In these cases, you should use explicit exception chaining from the
        earlier error, or suppress it with `raise ... from None`.  See
        https://docs.python.org/3/tutorial/errors.html#exception-chaining
        """
        if (
            node.cause is None
            and node.exc is not None
            and not (isinstance(node.exc, ast.Name) and node.exc.id.islower())
            and any(isinstance(n, ast.ExceptHandler) for n in self.node_stack)
        ):
            self.errors.append(
                B904(node.lineno, node.col_offset, vars=(self.in_trystar,))
            )

    def walk_function_body(self, node):
        def _loop(parent, node):
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                return
            yield parent, node
            for child in ast.iter_child_nodes(node):
                yield from _loop(node, child)

        for child in node.body:
            yield from _loop(node, child)

    def check_for_b901(self, node: ast.FunctionDef) -> None:
        if node.name == "__await__":
            return

        # If the user explicitly wrote the 3-argument version of Generator as the
        # return annotation, they probably know what they were doing.
        if (
            node.returns is not None
            and isinstance(node.returns, ast.Subscript)
            and (
                is_name(node.returns.value, "Generator")
                or is_name(node.returns.value, "typing.Generator")
                or is_name(node.returns.value, "collections.abc.Generator")
            )
        ):
            slice = node.returns.slice
            if sys.version_info < (3, 9) and isinstance(slice, ast.Index):
                slice = slice.value
            if isinstance(slice, ast.Tuple) and len(slice.elts) == 3:
                return

        has_yield = False
        return_node = None

        for parent, x in self.walk_function_body(node):
            # Only consider yield when it is part of an Expr statement.
            if isinstance(parent, ast.Expr) and isinstance(
                x, (ast.Yield, ast.YieldFrom)
            ):
                has_yield = True

            if isinstance(x, ast.Return) and x.value is not None:
                return_node = x

        if has_yield and return_node is not None:
            self.errors.append(B901(return_node.lineno, return_node.col_offset))

    # taken from pep8-naming
    @classmethod
    def find_decorator_name(cls, d):
        if isinstance(d, ast.Name):
            return d.id
        elif isinstance(d, ast.Attribute):
            return d.attr
        elif isinstance(d, ast.Call):
            return cls.find_decorator_name(d.func)

    def check_for_b902(  # noqa: C901 (too complex)
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> None:
        def is_classmethod(decorators: Set[str]) -> bool:
            return (
                any(name in decorators for name in self.b902_classmethod_decorators)
                or node.name in B902_IMPLICIT_CLASSMETHODS
            )

        if len(self.contexts) < 2 or not isinstance(
            self.contexts[-2].node, ast.ClassDef
        ):
            return

        cls = self.contexts[-2].node

        decorators: set[str] = {
            self.find_decorator_name(d) for d in node.decorator_list
        }

        if "staticmethod" in decorators:
            # TODO: maybe warn if the first argument is surprisingly `self` or
            # `cls`?
            return

        bases = {b.id for b in cls.bases if isinstance(b, ast.Name)}
        if any(basetype in bases for basetype in ("type", "ABCMeta", "EnumMeta")):
            if is_classmethod(decorators):
                expected_first_args = B902_METACLS
                kind = "metaclass class"
            else:
                expected_first_args = B902_CLS
                kind = "metaclass instance"
        else:
            if is_classmethod(decorators):
                expected_first_args = B902_CLS
                kind = "class"
            else:
                expected_first_args = B902_SELF
                kind = "instance"

        args = getattr(node.args, "posonlyargs", []) + node.args.args
        vararg = node.args.vararg
        kwarg = node.args.kwarg
        kwonlyargs = node.args.kwonlyargs

        if args:
            actual_first_arg = args[0].arg
            lineno = args[0].lineno
            col = args[0].col_offset
        elif vararg:
            actual_first_arg = "*" + vararg.arg
            lineno = vararg.lineno
            col = vararg.col_offset
        elif kwarg:
            actual_first_arg = "**" + kwarg.arg
            lineno = kwarg.lineno
            col = kwarg.col_offset
        elif kwonlyargs:
            actual_first_arg = "*, " + kwonlyargs[0].arg
            lineno = kwonlyargs[0].lineno
            col = kwonlyargs[0].col_offset
        else:
            actual_first_arg = "(none)"
            lineno = node.lineno
            col = node.col_offset

        if actual_first_arg not in expected_first_args:
            if not actual_first_arg.startswith(("(", "*")):
                actual_first_arg = repr(actual_first_arg)
            self.errors.append(
                B902(lineno, col, vars=(actual_first_arg, kind, expected_first_args[0]))
            )

    def check_for_b903(self, node) -> None:
        body = node.body
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            # Ignore the docstring
            body = body[1:]

        if (
            len(body) != 1
            or not isinstance(body[0], ast.FunctionDef)
            or body[0].name != "__init__"
        ):
            # only classes with *just* an __init__ method are interesting
            return

        # all the __init__ function does is a series of assignments to attributes
        for stmt in body[0].body:
            if not isinstance(stmt, ast.Assign):
                return
            targets = stmt.targets
            if len(targets) > 1 or not isinstance(targets[0], ast.Attribute):
                return
            if not isinstance(stmt.value, ast.Name):
                return

        self.errors.append(B903(node.lineno, node.col_offset))

    def check_for_b018(self, node) -> None:
        if not isinstance(node, ast.Expr):
            return
        if isinstance(
            node.value,
            (
                ast.List,
                ast.Set,
                ast.Dict,
                ast.Tuple,
            ),
        ) or (
            isinstance(node.value, ast.Constant)
            and (
                isinstance(node.value.value, (int, float, complex, bytes, bool))
                or node.value.value is None
            )
        ):
            self.errors.append(
                B018(
                    node.lineno,
                    node.col_offset,
                    vars=(node.value.__class__.__name__,),
                )
            )

    def check_for_b021(self, node) -> None:
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.JoinedStr)
        ):
            self.errors.append(
                B021(node.body[0].value.lineno, node.body[0].value.col_offset)
            )

    def check_for_b022(self, node) -> None:
        item = node.items[0]
        item_context = item.context_expr
        if (
            hasattr(item_context, "func")
            and hasattr(item_context.func, "value")
            and hasattr(item_context.func.value, "id")
            and item_context.func.value.id == "contextlib"
            and hasattr(item_context.func, "attr")
            and item_context.func.attr == "suppress"
            and len(item_context.args) == 0
        ):
            self.errors.append(B022(node.lineno, node.col_offset))

    @staticmethod
    def _is_assertRaises_like(node: ast.withitem) -> bool:
        if not (
            isinstance(node, ast.withitem)
            and isinstance(node.context_expr, ast.Call)
            and isinstance(node.context_expr.func, (ast.Attribute, ast.Name))
        ):
            return False
        if isinstance(node.context_expr.func, ast.Name):
            # "with raises"
            return node.context_expr.func.id in B908_pytest_functions
        elif isinstance(node.context_expr.func, ast.Attribute) and isinstance(
            node.context_expr.func.value, ast.Name
        ):
            return (
                # "with pytest.raises"
                node.context_expr.func.value.id == "pytest"
                and node.context_expr.func.attr in B908_pytest_functions
            ) or (
                # "with self.assertRaises"
                node.context_expr.func.value.id == "self"
                and node.context_expr.func.attr in B908_unittest_methods
            )
        else:
            return False

    def check_for_b908(self, node: ast.With) -> None:
        if len(node.body) < 2:
            return
        for node_item in node.items:
            if self._is_assertRaises_like(node_item):
                self.errors.append(B908(node.lineno, node.col_offset))

    def check_for_b025(self, node) -> None:
        seen = []
        for handler in node.handlers:
            if isinstance(handler.type, (ast.Name, ast.Attribute)):
                name = ".".join(compose_call_path(handler.type))
                seen.append(name)
            elif isinstance(handler.type, ast.Tuple):
                # to avoid checking the same as B014, remove duplicates per except
                uniques = set()
                for entry in handler.type.elts:
                    name = ".".join(compose_call_path(entry))
                    uniques.add(name)
                seen.extend(uniques)
        # sort to have a deterministic output
        duplicates = sorted({x for x in seen if seen.count(x) > 1})
        for duplicate in duplicates:
            self.errors.append(
                B025(node.lineno, node.col_offset, vars=(duplicate, self.in_trystar))
            )

    @staticmethod
    def _is_infinite_iterator(node: ast.expr) -> bool:
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "itertools"
        ):
            return False
        if node.func.attr in {"cycle", "count"}:
            return True
        elif node.func.attr == "repeat":
            if len(node.args) == 1 and len(node.keywords) == 0:
                # itertools.repeat(iterable)
                return True
            if (
                len(node.args) == 2
                and isinstance(node.args[1], ast.Constant)
                and node.args[1].value is None
            ):
                # itertools.repeat(iterable, None)
                return True
            for kw in node.keywords:
                # itertools.repeat(iterable, times=None)
                if (
                    kw.arg == "times"
                    and isinstance(kw.value, ast.Constant)
                    and kw.value.value is None
                ):
                    return True

        return False

    def check_for_b905(self, node) -> None:
        if not (isinstance(node.func, ast.Name) and node.func.id == "zip"):
            return
        for arg in node.args:
            if self._is_infinite_iterator(arg):
                return
        if not any(kw.arg == "strict" for kw in node.keywords):
            self.errors.append(B905(node.lineno, node.col_offset))

    def check_for_b906(self, node: ast.FunctionDef) -> None:
        if not node.name.startswith("visit_"):
            return

        # extract what's visited
        class_name = node.name[len("visit_") :]

        # silence any DeprecationWarnings
        # that might come from accessing a deprecated AST node
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            class_type = getattr(ast, class_name, None)

        if (
            # not a valid ast subclass
            class_type is None
            # doesn't have a non-empty '_fields' attribute - which is what's
            # iterated over in ast.NodeVisitor.generic_visit
            or not getattr(class_type, "_fields", None)
            # or can't contain any ast subnodes that could be visited
            # See https://docs.python.org/3/library/ast.html#abstract-grammar
            or class_type.__name__
            in (
                "alias",
                "Constant",
                "Global",
                "MatchSingleton",
                "MatchStar",
                "Nonlocal",
                "TypeIgnore",
                # These ast nodes are deprecated, but some codebases may still use them
                # for backwards-compatibility with Python 3.7
                "Bytes",
                "Num",
                "Str",
            )
        ):
            return

        for n in itertools.chain.from_iterable(ast.walk(nn) for nn in node.body):
            if isinstance(n, ast.Call) and (
                (isinstance(n.func, ast.Attribute) and "visit" in n.func.attr)
                or (isinstance(n.func, ast.Name) and "visit" in n.func.id)
            ):
                break
        else:
            self.errors.append(B906(node.lineno, node.col_offset))

    def check_for_b907(self, node: ast.JoinedStr) -> None:  # noqa: C901
        def myunparse(node: ast.AST) -> str:  # pragma: no cover
            if sys.version_info >= (3, 9):
                return ast.unparse(node)
            if isinstance(node, ast.Name):
                return node.id
            if isinstance(node, ast.Attribute):
                return myunparse(node.value) + "." + node.attr
            if isinstance(node, ast.Constant):
                return repr(node.value)
            if isinstance(node, ast.Call):
                return myunparse(node.func) + "()"  # don't bother with arguments

            # as a last resort, just give the type name
            return type(node).__name__

        quote_marks = "'\""
        current_mark = None
        variable = None
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                if not value.value:
                    continue

                # check for quote mark after pre-marked variable
                if (
                    current_mark is not None
                    and variable is not None
                    and value.value[0] == current_mark
                ):
                    self.errors.append(
                        B907(
                            variable.lineno,
                            variable.col_offset,
                            vars=(myunparse(variable.value),),
                        )
                    )
                    current_mark = variable = None
                    # don't continue with length>1, so we can detect a new pre-mark
                    # in the same string as a post-mark, e.g. `"{foo}" "{bar}"`
                    if len(value.value) == 1:
                        continue

                # detect pre-mark
                if value.value[-1] in quote_marks:
                    current_mark = value.value[-1]
                    variable = None
                    continue

            # detect variable, if there's a pre-mark
            if (
                current_mark is not None
                and variable is None
                and isinstance(value, ast.FormattedValue)
                and value.conversion != ord("r")
            ):
                # check if the format spec shows that this is numeric
                # or otherwise hard/impossible to convert to `!r`
                if (
                    isinstance(value.format_spec, ast.JoinedStr)
                    and value.format_spec.values  # empty format spec is fine
                ):
                    if (
                        # if there's variables in the format_spec, skip
                        len(value.format_spec.values) > 1
                        or not isinstance(value.format_spec.values[0], ast.Constant)
                    ):
                        current_mark = variable = None
                        continue
                    format_specifier = value.format_spec.values[0].value

                    # if second character is an align, first character is a fill
                    # char - strip it
                    if len(format_specifier) > 1 and format_specifier[1] in "<>=^":
                        format_specifier = format_specifier[1:]

                    # strip out precision digits, so the only remaining ones are
                    # width digits, which will misplace the quotes
                    format_specifier = re.sub(r"\.\d*", "", format_specifier)

                    # skip if any invalid characters in format spec
                    invalid_characters = "".join(
                        (
                            "=",  # align character only valid for numerics
                            "+- ",  # sign
                            "0123456789",  # width digits
                            "z",  # coerce negative zero floating point to positive
                            "#",  # alternate form
                            "_,",  # thousands grouping
                            "bcdeEfFgGnoxX%",  # various number specifiers
                        )
                    )
                    if set(format_specifier).intersection(invalid_characters):
                        current_mark = variable = None
                        continue

                # otherwise save value as variable
                variable = value
                continue

            # if no pre-mark or variable detected, reset state
            current_mark = variable = None

    def check_for_b028(self, node) -> None:
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "warn"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "warnings"
            and not any(kw.arg == "stacklevel" for kw in node.keywords)
            and not any(kw.arg == "skip_file_prefixes" for kw in node.keywords)
            and len(node.args) < 3
            and not any(isinstance(a, ast.Starred) for a in node.args)
            and not any(kw.arg is None for kw in node.keywords)
        ):
            self.errors.append(B028(node.lineno, node.col_offset))

    def check_for_b032(self, node) -> None:
        if (
            node.value is None
            and hasattr(node.target, "value")
            and isinstance(node.target.value, ast.Name)
            and (
                isinstance(node.target, ast.Subscript)
                or (
                    isinstance(node.target, ast.Attribute)
                    and node.target.value.id != "self"
                )
            )
        ):
            self.errors.append(B032(node.lineno, node.col_offset))

    def check_for_b033(self, node) -> None:
        seen = set()
        for elt in node.elts:
            if not isinstance(elt, ast.Constant):
                continue
            if elt.value in seen:
                self.errors.append(
                    B033(elt.lineno, elt.col_offset, vars=(repr(elt.value),))
                )
            else:
                seen.add(elt.value)

    def check_for_b034(self, node: ast.Call) -> None:
        if not isinstance(node.func, ast.Attribute):
            return
        func = node.func
        if not isinstance(func.value, ast.Name) or func.value.id != "re":
            return

        def check(num_args: int, param_name: str) -> None:
            if len(node.args) > num_args:
                arg = node.args[num_args]
                self.errors.append(
                    B034(arg.lineno, arg.col_offset, vars=(func.attr, param_name))
                )

        if func.attr in ("sub", "subn"):
            check(3, "count")
        elif func.attr == "split":
            check(2, "maxsplit")

    def check_for_b909(self, node: ast.For) -> None:
        if isinstance(node.iter, ast.Name):
            name = _to_name_str(node.iter)
            key = _to_name_str(node.target)
        elif isinstance(node.iter, ast.Attribute):
            name = _to_name_str(node.iter)
            key = _to_name_str(node.target)
        else:
            return
        checker = B909Checker(name, key)
        checker.visit(node.body)
        for mutation in itertools.chain.from_iterable(
            m for m in checker.mutations.values()
        ):
            self.errors.append(B909(mutation.lineno, mutation.col_offset))

    def check_for_b910(self, node: ast.Call) -> None:
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "defaultdict"
            and len(node.args) > 0
            and isinstance(node.args[0], ast.Name)
            and node.args[0].id == "int"
        ):
            self.errors.append(B910(node.lineno, node.col_offset))

    def check_for_b911(self, node: ast.Call) -> None:
        if (
            (isinstance(node.func, ast.Name) and node.func.id == "batched")
            or (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "batched"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "itertools"
            )
        ) and not any(kw.arg == "strict" for kw in node.keywords):
            self.errors.append(B911(node.lineno, node.col_offset))


def compose_call_path(node):
    if isinstance(node, ast.Attribute):
        yield from compose_call_path(node.value)
        yield node.attr
    elif isinstance(node, ast.Call):
        yield from compose_call_path(node.func)
    elif isinstance(node, ast.Name):
        yield node.id


def is_name(node: ast.expr, name: str) -> bool:
    if "." not in name:
        return isinstance(node, ast.Name) and node.id == name
    else:
        if not isinstance(node, ast.Attribute):
            return False
        rest, attr = name.rsplit(".", maxsplit=1)
        return node.attr == attr and is_name(node.value, rest)


def _transform_slice_to_py39(slice: ast.expr | ast.Slice) -> ast.Slice | ast.expr:
    """Transform a py38 style slice to a py39 style slice.

    In py39 the slice was changed to have simple names directly assigned:
    ```py
    # code:
    some_dict[key]
    # py38:
    slice=Index(
        value=Name(
                lineno=152,
                col_offset=14,
                end_lineno=152,
                end_col_offset=17,
                id='key',
                ctx=Load()
            ),
    )
    # py39 onwards:
    slice=Name(
                lineno=152,
                col_offset=14,
                end_lineno=152,
                end_col_offset=17,
                id='key',
                ctx=Load()
            ),
    ```

    > Changed in version 3.9: Simple indices are represented by their value,
    > extended slices are represented as tuples.
    from https://docs.python.org/3/library/ast.html#module-ast
    """
    if sys.version_info >= (3, 9):
        return slice
    if isinstance(slice, ast.Index) and isinstance(slice.value, ast.Name):
        slice = slice.value
    return slice


class B909Checker(ast.NodeVisitor):
    # https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types
    MUTATING_FUNCTIONS = (
        "append",
        "sort",
        "reverse",
        "remove",
        "clear",
        "extend",
        "insert",
        "pop",
        "popitem",
        "setdefault",
        "update",
        "intersection_update",
        "difference_update",
        "symmetric_difference_update",
        "add",
        "discard",
    )

    def __init__(self, name: str, key: str) -> None:
        self.name = name
        self.key = key
        self.mutations: dict[int, list[ast.AST]] = defaultdict(list)
        self._conditional_block = 0

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            if (
                isinstance(target, ast.Subscript)
                and _to_name_str(target.value) == self.name
                and _to_name_str(_transform_slice_to_py39(target.slice)) != self.key
            ):
                self.mutations[self._conditional_block].append(node)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        if _to_name_str(node.target) == self.name:
            self.mutations[self._conditional_block].append(node)
        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete) -> None:
        for target in node.targets:
            if isinstance(target, ast.Subscript):
                name = _to_name_str(target.value)
            elif isinstance(target, (ast.Attribute, ast.Name)):
                name = ""  # ignore "del foo"
            else:
                name = ""  # fallback
                self.generic_visit(target)

            if name == self.name:
                self.mutations[self._conditional_block].append(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Attribute):
            name = _to_name_str(node.func.value)
            function_object = name
            function_name = node.func.attr

            if (
                function_object == self.name
                and function_name in self.MUTATING_FUNCTIONS
            ):
                self.mutations[self._conditional_block].append(node)

        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        self._conditional_block += 1
        self.visit(node.body)
        self._conditional_block += 1

    def visit(self, node):
        """Like super-visit but supports iteration over lists."""
        if not isinstance(node, list):
            return super().visit(node)

        for elem in node:
            if isinstance(elem, ast.Break):
                self.mutations[self._conditional_block].clear()
            self.visit(elem)
        return node


@attr.s
class NameFinder(ast.NodeVisitor):
    """Finds a name within a tree of nodes.

    After `.visit(node)` is called, `found` is a dict with all name nodes inside,
    key is name string, value is the node (useful for location purposes).
    """

    names: Dict[str, List[ast.Name]] = attr.ib(factory=dict)

    def visit_Name(  # noqa: B906 # names don't contain other names
        self, node: ast.Name
    ) -> None:
        self.names.setdefault(node.id, []).append(node)

    def visit(self, node):
        """Like super-visit but supports iteration over lists."""
        if not isinstance(node, list):
            return super().visit(node)

        for elem in node:
            super().visit(elem)
        return node


@attr.s
class NamedExprFinder(ast.NodeVisitor):
    """Finds names defined through an ast.NamedExpr.

    After `.visit(node)` is called, `found` is a dict with all name nodes inside,
    key is name string, value is the node (useful for location purposes).
    """

    names: Dict[str, List[ast.Name]] = attr.ib(factory=dict)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        self.names.setdefault(node.target.id, []).append(node.target)
        self.generic_visit(node)

    def visit(self, node):
        """Like super-visit but supports iteration over lists."""
        if not isinstance(node, list):
            return super().visit(node)

        for elem in node:
            super().visit(elem)
        return node


class FunctionDefDefaultsVisitor(ast.NodeVisitor):
    """Used by B006, B008, and B039. B039 is essentially B006+B008 but for ContextVar."""

    def __init__(
        self,
        error_code_calls,  # B006 or B039
        error_code_literals,  # B008 or B039
        b008_b039_extend_immutable_calls=None,
    ) -> None:
        self.b008_b039_extend_immutable_calls = (
            b008_b039_extend_immutable_calls or set()
        )
        self.error_code_calls = error_code_calls
        self.error_code_literals = error_code_literals
        for node in B006_MUTABLE_LITERALS + B006_MUTABLE_COMPREHENSIONS:
            setattr(self, f"visit_{node}", self.visit_mutable_literal_or_comprehension)
        self.errors: list[error] = []
        self.arg_depth = 0
        super().__init__()

    def visit_mutable_literal_or_comprehension(self, node) -> None:
        # Flag B006 iff mutable literal/comprehension is not nested.
        # We only flag these at the top level of the expression as we
        # cannot easily guarantee that nested mutable structures are not
        # made immutable by outer operations, so we prefer no false positives.
        # e.g.
        # >>> def this_is_fine(a=frozenset({"a", "b", "c"})): ...
        #
        # >>> def this_is_not_fine_but_hard_to_detect(a=(lambda x: x)([1, 2, 3]))
        #
        # We do still search for cases of B008 within mutable structures though.
        if self.arg_depth == 1:
            self.errors.append(self.error_code_calls(node.lineno, node.col_offset))
        # Check for nested functions.
        self.generic_visit(node)

    def visit_Call(self, node) -> None:
        call_path = ".".join(compose_call_path(node.func))
        if call_path in B006_MUTABLE_CALLS:
            self.errors.append(self.error_code_calls(node.lineno, node.col_offset))
            self.generic_visit(node)
            return

        if call_path in B008_IMMUTABLE_CALLS | self.b008_b039_extend_immutable_calls:
            self.generic_visit(node)
            return

        # Check if function call is actually a float infinity/NaN literal
        if call_path == "float" and len(node.args) == 1:
            try:
                value = float(ast.literal_eval(node.args[0]))
            except Exception:
                pass
            else:
                if math.isfinite(value):
                    self.errors.append(
                        self.error_code_literals(node.lineno, node.col_offset)
                    )
        else:
            self.errors.append(self.error_code_literals(node.lineno, node.col_offset))

        # Check for nested functions.
        self.generic_visit(node)

    def visit_Lambda(self, node) -> None:  # noqa: B906
        # Don't recurse into lambda expressions
        # as they are evaluated at call time.
        pass

    def visit(self, node) -> None:
        """Like super-visit but supports iteration over lists."""
        self.arg_depth += 1
        if isinstance(node, list):
            for elem in node:
                if elem is not None:
                    super().visit(elem)
        else:
            super().visit(node)
        self.arg_depth -= 1


class B020NameFinder(NameFinder):
    """Ignore names defined within the local scope of a comprehension."""

    def visit_GeneratorExp(self, node) -> None:
        self.visit(node.generators)

    def visit_ListComp(self, node) -> None:
        self.visit(node.generators)

    def visit_DictComp(self, node) -> None:
        self.visit(node.generators)

    def visit_comprehension(self, node) -> None:
        self.visit(node.iter)

    def visit_Lambda(self, node) -> None:
        self.visit(node.body)
        for lambda_arg in node.args.args:
            self.names.pop(lambda_arg.arg, None)


error = namedtuple("error", "lineno col message type vars")
Error = partial(partial, error, type=BugBearChecker, vars=())

# note: bare except* is a syntax error, so B001 does not need to handle it
B001 = Error(
    message=(
        "B001 Do not use bare `except:`, it also catches unexpected "
        "events like memory errors, interrupts, system exit, and so on.  "
        "Prefer excepting specific exceptions  If you're sure what you're "
        "doing, be explicit and write `except BaseException:`."
    )
)

B002 = Error(
    message=(
        "B002 Python does not support the unary prefix increment. Writing "
        "++n is equivalent to +(+(n)), which equals n. You meant n += 1."
    )
)

B003 = Error(
    message=(
        "B003 Assigning to `os.environ` doesn't clear the environment. "
        "Subprocesses are going to see outdated variables, in disagreement "
        "with the current process. Use `os.environ.clear()` or the `env=` "
        "argument to Popen."
    )
)

B004 = Error(
    message=(
        "B004 Using `hasattr(x, '__call__')` to test if `x` is callable "
        "is unreliable. If `x` implements custom `__getattr__` or its "
        "`__call__` is itself not callable, you might get misleading "
        "results. Use `callable(x)` for consistent results."
    )
)

B005 = Error(
    message=(
        "B005 Using .strip() with multi-character strings is misleading "
        "the reader. It looks like stripping a substring. Move your "
        "character set to a constant if this is deliberate. Use "
        ".replace(), .removeprefix(), .removesuffix(), or regular "
        "expressions to remove string fragments."
    )
)
B005_METHODS = {"lstrip", "rstrip", "strip"}

B006 = Error(
    message=(
        "B006 Do not use mutable data structures for argument defaults.  They "
        "are created during function definition time. All calls to the function "
        "reuse this one instance of that data structure, persisting changes "
        "between them."
    )
)

# Note: these are also used by B039
B006_MUTABLE_LITERALS = ("Dict", "List", "Set")
B006_MUTABLE_COMPREHENSIONS = ("ListComp", "DictComp", "SetComp")
B006_MUTABLE_CALLS = {
    "Counter",
    "OrderedDict",
    "collections.Counter",
    "collections.OrderedDict",
    "collections.defaultdict",
    "collections.deque",
    "defaultdict",
    "deque",
    "dict",
    "list",
    "set",
}
B007 = Error(
    message=(
        "B007 Loop control variable {!r} not used within the loop body. "
        "If this is intended, start the name with an underscore."
    )
)
B008 = Error(
    message=(
        "B008 Do not perform function calls in argument defaults.  The call is "
        "performed only once at function definition time. All calls to your "
        "function will reuse the result of that definition-time function call.  If "
        "this is intended, assign the function call to a module-level variable and "
        "use that variable as a default value."
    )
)

# Note: these are also used by B039
B008_IMMUTABLE_CALLS = {
    "tuple",
    "frozenset",
    "types.MappingProxyType",
    "MappingProxyType",
    "re.compile",
    "operator.attrgetter",
    "operator.itemgetter",
    "operator.methodcaller",
    "attrgetter",
    "itemgetter",
    "methodcaller",
}
B009 = Error(
    message=(
        "B009 Do not call getattr with a constant attribute value, "
        "it is not any safer than normal property access."
    )
)
B010 = Error(
    message=(
        "B010 Do not call setattr with a constant attribute value, "
        "it is not any safer than normal property access."
    )
)
B011 = Error(
    message=(
        "B011 Do not call assert False since python -O removes these calls. "
        "Instead callers should raise AssertionError()."
    )
)
B012 = Error(
    message=(
        "B012 return/continue/break inside finally blocks cause exceptions "
        "to be silenced. Exceptions should be silenced in except{0} blocks. Control "
        "statements can be moved outside the finally block."
    )
)
B013 = Error(
    message=(
        "B013 A length-one tuple literal is redundant.  "
        "Write `except{1} {0}:` instead of `except{1} ({0},):`."
    )
)
B014 = Error(
    message=(
        "B014 Redundant exception types in `except{3} ({0}){1}:`.  "
        "Write `except{3} {2}{1}:`, which catches exactly the same exceptions."
    )
)
B014_REDUNDANT_EXCEPTIONS = {
    "OSError": {
        # All of these are actually aliases of OSError since Python 3.3
        "IOError",
        "EnvironmentError",
        "WindowsError",
        "mmap.error",
        "socket.error",
        "select.error",
    },
    "ValueError": {
        "binascii.Error",
    },
}
B015 = Error(
    message=(
        "B015 Result of comparison is not used. This line doesn't do "
        "anything. Did you intend to prepend it with assert?"
    )
)
B016 = Error(
    message=(
        "B016 Cannot raise a literal. Did you intend to return it or raise "
        "an Exception?"
    )
)
B017 = Error(
    message=(
        "B017 `assertRaises(Exception)` and `pytest.raises(Exception)` should "
        "be considered evil. They can lead to your test passing even if the "
        "code being tested is never executed due to a typo. Assert for a more "
        "specific exception (builtin or custom), or use `assertRaisesRegex` "
        "(if using `assertRaises`), or add the `match` keyword argument (if "
        "using `pytest.raises`), or use the context manager form with a target."
    )
)
B018 = Error(
    message=(
        "B018 Found useless {} expression. Consider either assigning it to a "
        "variable or removing it."
    )
)
B019 = Error(
    message=(
        "B019 Use of `functools.lru_cache` or `functools.cache` on methods "
        "can lead to memory leaks. The cache may retain instance references, "
        "preventing garbage collection."
    )
)
B019_CACHES = {
    "functools.cache",
    "functools.lru_cache",
    "cache",
    "lru_cache",
}
B020 = Error(
    message=(
        "B020 Found for loop that reassigns the iterable it is iterating "
        + "with each iterable value."
    )
)
B021 = Error(
    message=(
        "B021 f-string used as docstring. "
        "This will be interpreted by python as a joined string rather than a docstring."
    )
)
B022 = Error(
    message=(
        "B022 No arguments passed to `contextlib.suppress`. "
        "No exceptions will be suppressed and therefore this "
        "context manager is redundant."
    )
)

B023 = Error(message="B023 Function definition does not bind loop variable {!r}.")
B024 = Error(
    message=(
        "B024 {} is an abstract base class, but none of the methods it defines are"
        " abstract. This is not necessarily an error, but you might have forgotten to"
        " add the @abstractmethod decorator, potentially in conjunction with"
        " @classmethod, @property and/or @staticmethod."
    )
)
B025 = Error(
    message=(
        "B025 Exception `{0}` has been caught multiple times. Only the first except{0}"
        " will be considered and all other except{0} catches can be safely removed."
    )
)
B026 = Error(
    message=(
        "B026 Star-arg unpacking after a keyword argument is strongly discouraged, "
        "because it only works when the keyword parameter is declared after all "
        "parameters supplied by the unpacked sequence, and this change of ordering can "
        "surprise and mislead readers."
    )
)
B027 = Error(
    message=(
        "B027 {} is an empty method in an abstract base class, but has no abstract"
        " decorator. Consider adding @abstractmethod."
    )
)
B028 = Error(
    message=(
        "B028 No explicit stacklevel argument found. The warn method from the"
        " warnings module uses a stacklevel of 1 by default. This will only show a"
        " stack trace for the line on which the warn method is called."
        " It is therefore recommended to use a stacklevel of 2 or"
        " greater to provide more information to the user."
    )
)
B029 = Error(
    message=(
        "B029 Using `except{0} ():` with an empty tuple does not handle/catch "
        "anything. Add exceptions to handle."
    )
)

B030 = Error(message="B030 Except handlers should only be names of exception classes")

B031 = Error(
    message=(
        "B031 Using the generator returned from `itertools.groupby()` more than once"
        " will do nothing on the second usage. Save the result to a list, if the"
        " result is needed multiple times."
    )
)

B032 = Error(
    message=(
        "B032 Possible unintentional type annotation (using `:`). Did you mean to"
        " assign (using `=`)?"
    )
)

B033 = Error(
    message=(
        "B033 Set should not contain duplicate item {}. Duplicate items will be"
        " replaced with a single item at runtime."
    )
)

B034 = Error(
    message=(
        "B034 {} should pass `{}` and `flags` as keyword arguments to avoid confusion"
        " due to unintuitive argument positions."
    )
)
B035 = Error(message="B035 Static key in dict comprehension {!r}.")

B036 = Error(
    message="B036 Don't except `BaseException` unless you plan to re-raise it."
)

B037 = Error(
    message="B037 Class `__init__` methods must not return or yield any values."
)

B039 = Error(
    message=(
        "B039 ContextVar with mutable literal or function call as default. "
        "This is only evaluated once, and all subsequent calls to `.get()` "
        "will return the same instance of the default."
    )
)

B040 = Error(
    message="B040 Exception with added note not used. Did you forget to raise it?"
)

B041 = Error(message=("B041 Repeated key-value pair in dictionary literal."))

# Warnings disabled by default.
B901 = Error(
    message=(
        "B901 Using `yield` together with `return x`. Use native "
        "`async def` coroutines or put a `# noqa` comment on this "
        "line if this was intentional."
    )
)
B902 = Error(
    message=(
        "B902 Invalid first argument {} used for {} method. Use the "
        "canonical first argument name in methods, i.e. {}."
    )
)
B902_IMPLICIT_CLASSMETHODS = {"__new__", "__init_subclass__", "__class_getitem__"}
B902_SELF = ["self"]  # it's a list because the first is preferred
B902_CLS = ["cls", "klass"]  # ditto.
B902_METACLS = ["metacls", "metaclass", "typ", "mcs"]  # ditto.

B903 = Error(
    message=(
        "B903 Data class should either be immutable or use __slots__ to "
        "save memory. Use collections.namedtuple to generate an immutable "
        "class, or enumerate the attributes in a __slot__ declaration in "
        "the class to leave attributes mutable."
    )
)

B904 = Error(
    message=(
        "B904 Within an `except{0}` clause, raise exceptions with `raise ... from err` or"
        " `raise ... from None` to distinguish them from errors in exception handling. "
        " See https://docs.python.org/3/tutorial/errors.html#exception-chaining for"
        " details."
    )
)

B905 = Error(message="B905 `zip()` without an explicit `strict=` parameter.")

B906 = Error(
    message=(
        "B906 `visit_` function with no further calls to a visit function, which might"
        " prevent the `ast` visitor from properly visiting all nodes."
        " Consider adding a call to `self.generic_visit(node)`."
    )
)

B907 = Error(
    message=(
        "B907 {!r} is manually surrounded by quotes, consider using the `!r` conversion"
        " flag."
    )
)
B908 = Error(
    message=(
        "B908 assertRaises-type context should not contain more than one top-level"
        " statement."
    )
)
B909 = Error(
    message=(
        "B909 editing a loop's mutable iterable often leads to unexpected results/bugs"
    )
)
B910 = Error(
    message="B910 Use Counter() instead of defaultdict(int) to avoid excessive memory use"
)
B911 = Error(
    message="B911 `itertools.batched()` without an explicit `strict=` parameter."
)
B950 = Error(message="B950 line too long ({} > {} characters)")


disabled_by_default = [
    "B901",
    "B902",
    "B903",
    "B904",
    "B905",
    "B906",
    "B908",
    "B909",
    "B910",
    "B911",
    "B950",
]
