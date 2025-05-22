import ast
import itertools
import os
import re
import site
import subprocess
import unittest
from argparse import Namespace
from pathlib import Path

import pytest

from bugbear import (
    BugBearChecker,
    BugBearVisitor,
    error,
    error_codes,
)

test_files: list[tuple[str, Path]] = sorted(
    (f.stem.upper(), f)
    for f in (Path(__file__).parent).iterdir()
    if re.fullmatch(r"b\d\d\d.*\.py", f.name)
)


@pytest.mark.parametrize(("test", "path"), test_files, ids=[f[0] for f in test_files])
def test_eval(
    test: str,
    path: Path,
):
    print(test, path)
    content = path.read_text()
    expected, options = _parse_eval_file(test, content)
    assert expected
    tuple_expected = [
        (e.lineno, e.col, e.message.format(*e.vars), e.type) for e in expected
    ]

    bbc = BugBearChecker(filename=str(path), options=options)
    errors = [e for e in bbc.run() if (test == "B950" or not e[2].startswith("B950"))]
    errors.sort()
    assert errors == tuple_expected


def _parse_eval_file(test: str, content: str) -> tuple[list[error], Namespace | None]:

    # error_class: Any = eval(error_code)
    expected: list[error] = []
    options: Namespace | None = None

    for lineno, line in enumerate(content.split("\n"), start=1):
        if line.startswith("# OPTIONS:"):
            options = eval(f"Namespace({line[10:]})")

        # skip commented out lines
        if not line or (line[0] == "#" and test != "B950"):
            continue

        # skip lines that *don't* have a comment
        if "#" not in line:
            continue

        # get text between `error:` and (end of line or another comment)
        k = re.findall(r"(B\d\d\d):([^#]*)(?=#|$)", line)
        for err_code, err_args in k:
            # evaluate the arguments as if in a tuple
            args = eval(f"({err_args},)")
            assert args, "you must specify at least column"
            col, *vars = args
            assert isinstance(col, int), "column must be an int"
            error_class = error_codes[err_code]
            expected.append(error_class(lineno, col, vars=vars))
    return expected, options


class BugbearTestCase(unittest.TestCase):
    maxDiff = None

    def errors(self, *errors):
        return [BugBearChecker.adapt_error(e) for e in errors]

    # manual permutations to save overhead when doing >60k permutations
    # see format spec at
    # https://docs.python.org/3/library/string.html#format-specification-mini-language
    def test_b907_format_specifier_permutations(self):
        visitor = BugBearVisitor(filename="", lines="")

        for fields in itertools.product(
            (None, "x"),  # fill (any character)
            (None, *"<>=^"),  # align
            (None, *"+- "),  # sign
            (None, "z"),  # z_letter
            (None, "#"),  # pound_sign
            (None, "0"),  # zero
            (None, *"19"),  # width
            (None, *"_,"),  # grouping_option
            (None, ".8"),  # precision
            (None, *"bcdeEfFgGnosxX%"),  # type_
        ):
            format_spec = "".join(f for f in fields if f is not None)

            # directly interact with a visitor to save on runtime
            bbc_string = "f'\"{var:" + format_spec + "}\"'"
            tree = ast.parse(bbc_string)
            visitor.errors = []
            visitor.visit(tree)

            format_string = "'{:" + format_spec + "}'"
            try:
                old = format_string.format("hello")
            except ValueError:
                assert (
                    visitor.errors == []
                ), f"b907 raised for {format_spec!r} not valid for string"
                continue

            new = ("{!r:" + format_spec + "}").format("hello")

            # Preceding the width field by 0 in >=3.10 is valid, but does nothing.
            # The presence of it means likely numeric variable though.
            # A width shorter than the string will look the same, but should not give b907.
            if fields[5] == "0" or fields[6] == "1":
                assert (
                    visitor.errors == []
                ), f"b907 should not raise on questionable case {format_spec}"
            elif old == new:
                assert visitor.errors, (
                    f"b907 not raised for {format_spec} that would look identical"
                    " with !r"
                )
            else:
                assert (
                    visitor.errors == []
                ), f"b907 raised for {format_spec} that would look different with !r"

    def test_b9_select(self):
        filename = Path(__file__).absolute().parent / "b950.py"

        mock_options = Namespace(select=["B950"])
        bbc = BugBearChecker(filename=str(filename), options=mock_options)
        errors = list(bbc.run())
        B950 = error_codes["B950"]
        self.assertEqual(
            errors,
            self.errors(
                B950(7, 113, vars=(113, 79)),
                B950(12, 125, vars=(125, 79)),
                B950(14, 125, vars=(125, 79)),
                B950(21, 118, vars=(118, 79)),
                B950(36, 132, vars=(132, 79)),
                B950(37, 140, vars=(140, 79)),
            ),
        )

    def test_b9_extend_select(self):
        filename = Path(__file__).absolute().parent / "b950.py"

        # select is always going to have a value, usually the default codes, but can
        # also be empty
        mock_options = Namespace(select=[], extend_select=["B950"])
        bbc = BugBearChecker(filename=str(filename), options=mock_options)
        errors = list(bbc.run())
        B950 = error_codes["B950"]
        self.assertEqual(
            errors,
            self.errors(
                B950(7, 113, vars=(113, 79)),
                B950(12, 125, vars=(125, 79)),
                B950(14, 125, vars=(125, 79)),
                B950(21, 118, vars=(118, 79)),
                B950(36, 132, vars=(132, 79)),
                B950(37, 140, vars=(140, 79)),
            ),
        )

    def test_b9_flake8_next_default_options(self):
        filename = Path(__file__).absolute().parent / "b950.py"

        # in flake8 next, unset select / extend_select will be `None` to
        # signify the default values
        mock_options = Namespace(select=None, extend_select=None)
        bbc = BugBearChecker(filename=str(filename), options=mock_options)
        errors = list(bbc.run())
        self.assertEqual(errors, [])

    def test_selfclean_bugbear(self):
        filename = Path(__file__).absolute().parent.parent / "bugbear.py"
        proc = subprocess.run(
            ["flake8", str(filename)],
            capture_output=True,
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout.decode("utf8"))
        self.assertEqual(proc.stdout, b"")
        self.assertEqual(proc.stderr, b"")

    def test_selfclean_test_bugbear(self):
        filename = Path(__file__).absolute()
        proc = subprocess.run(
            ["flake8", str(filename)],
            capture_output=True,
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout.decode("utf8"))
        self.assertEqual(proc.stdout, b"")
        self.assertEqual(proc.stderr, b"")


class TestFuzz(unittest.TestCase):
    from hypothesis import HealthCheck, given, settings
    from hypothesmith import from_grammar

    @pytest.mark.filterwarnings("ignore::SyntaxWarning")
    @settings(suppress_health_check=[HealthCheck.too_slow])
    @given(from_grammar().map(ast.parse))
    def test_does_not_crash_on_any_valid_code(self, syntax_tree):
        # Given any syntatically-valid source code, flake8-bugbear should
        # not crash.  This tests doesn't check that we do the *right* thing,
        # just that we don't crash on valid-if-poorly-styled code!
        BugBearVisitor(filename="<string>", lines=[]).visit(syntax_tree)

    def test_does_not_crash_on_site_code(self):
        # Because the generator isn't perfect, we'll also test on all the code
        # we can easily find in our current Python environment - this includes
        # the standard library, and all installed packages.
        for base in sorted(set(site.PREFIXES)):
            for dirname, _, files in os.walk(base):
                for f in files:
                    if f.endswith(".py"):
                        BugBearChecker(filename=str(Path(dirname) / f))

    def test_does_not_crash_on_tuple_expansion_in_except_statement(self):
        # akin to test_does_not_crash_on_any_valid_code
        # but targets a rare case that's not covered by hypothesmith.from_grammar
        # see https://github.com/PyCQA/flake8-bugbear/issues/153
        syntax_tree = ast.parse(
            "grey_list = (ValueError,)\n"
            "black_list = (TypeError,)\n"
            "try:\n"
            "    int('1e3')\n"
            "except (*grey_list, *black_list):\n"
            "     print('error caught')"
        )
        BugBearVisitor(filename="<string>", lines=[]).visit(syntax_tree)

    def test_does_not_crash_on_call_in_except_statement(self):
        # akin to test_does_not_crash_on_tuple_expansion_in_except_statement
        # see https://github.com/PyCQA/flake8-bugbear/issues/171
        syntax_tree = ast.parse(
            "foo = lambda: IOError\ntry:\n    ...\nexcept (foo(),):\n    ...\n"
        )
        BugBearVisitor(filename="<string>", lines=[]).visit(syntax_tree)
