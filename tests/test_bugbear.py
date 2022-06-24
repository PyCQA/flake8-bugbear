import ast
import os
import site
import subprocess
import sys
import unittest
from argparse import Namespace
from pathlib import Path

from hypothesis import HealthCheck, given, settings
from hypothesmith import from_grammar

from bugbear import (
    B001,
    B002,
    B003,
    B004,
    B005,
    B006,
    B007,
    B008,
    B009,
    B010,
    B011,
    B012,
    B013,
    B014,
    B015,
    B016,
    B017,
    B018,
    B019,
    B020,
    B021,
    B022,
    B023,
    B901,
    B902,
    B903,
    B904,
    B950,
    BugBearChecker,
    BugBearVisitor,
)


class BugbearTestCase(unittest.TestCase):
    maxDiff = None

    def errors(self, *errors):
        return [BugBearChecker.adapt_error(e) for e in errors]

    def test_b001(self):
        filename = Path(__file__).absolute().parent / "b001.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B001(8, 0, vars=("bare `except:`",)),
            B001(40, 4, vars=("bare `except:`",)),
            B001(47, 0, vars=("`except ():`",)),
        )
        self.assertEqual(errors, expected)

    def test_b002(self):
        filename = Path(__file__).absolute().parent / "b002.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B002(15, 8), B002(20, 11)))

    def test_b003(self):
        filename = Path(__file__).absolute().parent / "b003.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B003(9, 0)))

    def test_b004(self):
        filename = Path(__file__).absolute().parent / "b004.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B004(3, 7), B004(5, 7)))

    def test_b005(self):
        filename = Path(__file__).absolute().parent / "b005.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B005(4, 0),
                B005(7, 0),
                B005(10, 0),
                B005(13, 0),
                B005(16, 0),
                B005(19, 0),
            ),
        )

    def test_b006_b008(self):
        filename = Path(__file__).absolute().parent / "b006_b008.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B006(60, 24),
                B006(64, 29),
                B006(68, 19),
                B006(72, 19),
                B006(76, 31),
                B006(80, 25),
                B006(85, 45 if sys.version_info >= (3, 8) else 46),
                B008(85, 60),
                B006(89, 45),
                B008(89, 63),
                B006(93, 44),
                B008(93, 59),
                B006(97, 32),
                B008(109, 38),
                B008(113, 11),
                B008(113, 31),
                B008(117, 29 if sys.version_info >= (3, 8) else 30),
                B008(160, 29),
                B008(164, 44),
                B006(170, 19),
                B008(170, 20),
                B008(170, 30),
                B008(176, 21),
                B008(181, 18),
                B008(181, 36),
            ),
        )

    def test_b007(self):
        filename = Path(__file__).absolute().parent / "b007.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B007(6, 4, vars=("i",)),
                B007(18, 12, vars=("k",)),
                B007(30, 4, vars=("i",)),
                B007(30, 12, vars=("k",)),
            ),
        )

    def test_b008_extended(self):
        filename = Path(__file__).absolute().parent / "b008_extended.py"

        mock_options = Namespace(
            extend_immutable_calls=["fastapi.Depends", "fastapi.Query"]
        )

        bbc = BugBearChecker(filename=str(filename), options=mock_options)
        errors = list(bbc.run())

        self.assertEqual(
            errors,
            self.errors(B008(15, 66)),
        )

    def test_b009_b010(self):
        filename = Path(__file__).absolute().parent / "b009_b010.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        all_errors = [
            B009(17, 0),
            B009(18, 0),
            B009(19, 0),
            B010(28, 0),
            B010(29, 0),
            B010(30, 0),
            B009(45, 14),
        ]
        self.assertEqual(errors, self.errors(*all_errors))

    def test_b011(self):
        filename = Path(__file__).absolute().parent / "b011.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors, self.errors(B011(8, 0, vars=("i",)), B011(10, 0, vars=("k",)))
        )

    def test_b012(self):
        filename = Path(__file__).absolute().parent / "b012.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        all_errors = [
            B012(5, 8),
            B012(13, 12),
            B012(21, 12),
            B012(31, 12),
            B012(44, 20),
            B012(66, 12),
            B012(78, 12),
            B012(94, 12),
            B012(101, 8),
            B012(107, 8),
        ]
        self.assertEqual(errors, self.errors(*all_errors))

    def test_b013(self):
        filename = Path(__file__).absolute().parent / "b013.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B013(10, 0, vars=("ValueError",)), B013(32, 0, vars=("re.error",))
        )
        self.assertEqual(errors, expected)

    def test_b014(self):
        filename = Path(__file__).absolute().parent / "b014.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B014(11, 0, vars=("Exception, TypeError", "", "Exception")),
            B014(17, 0, vars=("OSError, OSError", " as err", "OSError")),
            B014(28, 0, vars=("MyError, MyError", "", "MyError")),
            B014(42, 0, vars=("MyError, BaseException", " as e", "BaseException")),
            B014(49, 0, vars=("re.error, re.error", "", "re.error")),
            B014(
                56,
                0,
                vars=("IOError, EnvironmentError, OSError", "", "OSError"),
            ),
            B014(74, 0, vars=("ValueError, binascii.Error", "", "ValueError")),
        )
        self.assertEqual(errors, expected)

    def test_b015(self):
        filename = Path(__file__).absolute().parent / "b015.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(B015(8, 0), B015(12, 0), B015(22, 4), B015(29, 4))
        self.assertEqual(errors, expected)

    def test_b016(self):
        filename = Path(__file__).absolute().parent / "b016.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(B016(6, 0), B016(7, 0), B016(8, 0))
        self.assertEqual(errors, expected)

    def test_b017(self):
        filename = Path(__file__).absolute().parent / "b017.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(B017(22, 8))
        self.assertEqual(errors, expected)

    def test_b018_functions(self):
        filename = Path(__file__).absolute().parent / "b018_functions.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())

        expected = [B018(line, 4) for line in range(16, 26)]
        expected.append(B018(29, 4))
        expected.append(B018(32, 4))
        self.assertEqual(errors, self.errors(*expected))

    def test_b018_classes(self):
        filename = Path(__file__).absolute().parent / "b018_classes.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())

        expected = [B018(line, 4) for line in range(17, 27)]
        expected.append(B018(30, 4))
        expected.append(B018(33, 4))
        self.assertEqual(errors, self.errors(*expected))

    def test_b019(self):
        filename = Path(__file__).absolute().parent / "b019.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())

        # AST Decorator column location for callable decorators changes in 3.7
        col = 5 if sys.version_info >= (3, 7) else 4
        self.assertEqual(
            errors,
            self.errors(
                B019(73, 5),
                B019(77, 5),
                B019(81, col),
                B019(85, col),
                B019(89, 5),
                B019(93, 5),
                B019(97, col),
                B019(101, col),
            ),
        )

    def test_b020(self):
        filename = Path(__file__).absolute().parent / "b020.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B020(8, 4, vars=("items",)),
                B020(21, 9, vars=("values",)),
                B020(36, 4, vars=("vars",)),
            ),
        )

    def test_b021_classes(self):
        filename = Path(__file__).absolute().parent / "b021.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B021(14, 4),
            B021(22, 4),
            B021(30, 4),
            B021(38, 4),
            B021(46, 4),
            B021(54, 4),
            B021(62, 4),
            B021(70, 4),
            B021(74, 4),
        )
        self.assertEqual(errors, expected)

    def test_b022(self):
        filename = Path(__file__).absolute().parent / "b022.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B022(8, 0)))

    def test_b023(self):
        filename = Path(__file__).absolute().parent / "b023.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B023(12, 29, vars=("x",)),
            B023(13, 29, vars=("y",)),
            B023(16, 15, vars=("x",)),
            B023(28, 18, vars=("x",)),
            B023(29, 18, vars=("x",)),
            B023(30, 18, vars=("x",)),
            B023(31, 21, vars=("x",)),
            B023(40, 33, vars=("x",)),
            B023(42, 13, vars=("x",)),
            B023(50, 29, vars=("a",)),
            B023(51, 29, vars=("a_",)),
            B023(52, 29, vars=("b",)),
            B023(53, 29, vars=("c",)),
            B023(61, 16, vars=("j",)),
            B023(61, 20, vars=("k",)),
        )
        self.assertEqual(errors, expected)

    def test_b901(self):
        filename = Path(__file__).absolute().parent / "b901.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B901(9, 8), B901(36, 4)))

    def test_b902(self):
        filename = Path(__file__).absolute().parent / "b902.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B902(29, 17, vars=("'i_am_special'", "instance", "self")),
                B902(32, 30, vars=("'cls'", "instance", "self")),
                B902(35, 4, vars=("(none)", "instance", "self")),
                B902(39, 12, vars=("'self'", "class", "cls")),
                B902(42, 22, vars=("*args", "instance", "self")),
                B902(48, 30, vars=("**kwargs", "instance", "self")),
                B902(51, 32, vars=("*, self", "instance", "self")),
                B902(54, 44, vars=("*, self", "instance", "self")),
                B902(68, 17, vars=("'self'", "metaclass instance", "cls")),
                B902(72, 20, vars=("'cls'", "metaclass class", "metacls")),
            ),
        )

    @unittest.skipIf(sys.version_info < (3, 8), "requires 3.8+")
    def test_b902_py38(self):
        filename = Path(__file__).absolute().parent / "b902_py38.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B902(29, 17, vars=("'i_am_special'", "instance", "self")),
                B902(32, 30, vars=("'cls'", "instance", "self")),
                B902(35, 4, vars=("(none)", "instance", "self")),
                B902(39, 12, vars=("'self'", "class", "cls")),
                B902(42, 22, vars=("*args", "instance", "self")),
                B902(48, 30, vars=("**kwargs", "instance", "self")),
                B902(51, 32, vars=("*, self", "instance", "self")),
                B902(54, 44, vars=("*, self", "instance", "self")),
                B902(68, 17, vars=("'self'", "metaclass instance", "cls")),
                B902(72, 20, vars=("'cls'", "metaclass class", "metacls")),
            ),
        )

    def test_b903(self):
        filename = Path(__file__).absolute().parent / "b903.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B903(32, 0), B903(38, 0)))

    def test_b904(self):
        filename = Path(__file__).absolute().parent / "b904.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = [
            B904(10, 8),
            B904(11, 4),
            B904(16, 4),
            B904(55, 16),
        ]
        self.assertEqual(errors, self.errors(*expected))

    def test_b950(self):
        filename = Path(__file__).absolute().parent / "b950.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B950(7, 92, vars=(92, 79)),
                B950(12, 103, vars=(103, 79)),
                B950(14, 103, vars=(103, 79)),
                B950(21, 97, vars=(97, 79)),
            ),
        )

    def test_b9_select(self):
        filename = Path(__file__).absolute().parent / "b950.py"

        mock_options = Namespace(select=["B950"])
        bbc = BugBearChecker(filename=str(filename), options=mock_options)
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B950(7, 92, vars=(92, 79)),
                B950(12, 103, vars=(103, 79)),
                B950(14, 103, vars=(103, 79)),
                B950(21, 97, vars=(97, 79)),
            ),
        )

    def test_b9_extend_select(self):
        filename = Path(__file__).absolute().parent / "b950.py"

        # select is always going to have a value, usually the default codes, but can
        # also be empty
        mock_options = Namespace(select=[], extend_select=["B950"])
        bbc = BugBearChecker(filename=str(filename), options=mock_options)
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B950(7, 92, vars=(92, 79)),
                B950(12, 103, vars=(103, 79)),
                B950(14, 103, vars=(103, 79)),
                B950(21, 97, vars=(97, 79)),
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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout.decode("utf8"))
        self.assertEqual(proc.stdout, b"")
        self.assertEqual(proc.stderr, b"")

    def test_selfclean_test_bugbear(self):
        filename = Path(__file__).absolute()
        proc = subprocess.run(
            ["flake8", str(filename)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout.decode("utf8"))
        self.assertEqual(proc.stdout, b"")
        self.assertEqual(proc.stderr, b"")


class TestFuzz(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
