import ast
import itertools
import os
import site
import subprocess
import sys
import unittest
from argparse import Namespace
from pathlib import Path

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
    B024,
    B025,
    B026,
    B027,
    B028,
    B029,
    B030,
    B031,
    B032,
    B033,
    B034,
    B035,
    B036,
    B037,
    B901,
    B902,
    B903,
    B904,
    B905,
    B906,
    B907,
    B908,
    B909,
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
            B001(8, 0),
            B001(40, 4),
        )
        self.assertEqual(errors, expected)

    def test_b002(self):
        filename = Path(__file__).absolute().parent / "b002.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B002(14, 8), B002(19, 11)))

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
                B006(58, 24),
                B006(61, 29),
                B006(64, 19),
                B006(67, 19),
                B006(70, 31),
                B006(73, 25),
                B006(77, 45),
                B008(77, 60),
                B006(81, 45),
                B008(81, 63),
                B006(85, 44),
                B008(85, 59),
                B006(89, 32),
                B008(100, 38),
                B008(103, 11),
                B008(103, 31),
                B008(107, 29),
                B008(149, 29),
                B008(153, 44),
                B006(159, 19),
                B008(159, 20),
                B008(159, 30),
                B008(165, 21),
                B008(170, 18),
                B008(170, 36),
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
            self.errors(B008(13, 66)),
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
        expected = self.errors(B016(6, 0), B016(7, 0), B016(8, 0), B016(10, 0))
        self.assertEqual(errors, expected)

    def test_b017(self):
        filename = Path(__file__).absolute().parent / "b017.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B017(26, 8),
            B017(28, 8),
            B017(30, 8),
            B017(32, 8),
            B017(73, 8),
            B017(75, 8),
            B017(77, 8),
        )
        self.assertEqual(errors, expected)

    def test_b018_functions(self):
        filename = Path(__file__).absolute().parent / "b018_functions.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())

        expected = [
            B018(15, 4, vars=("Constant",)),
            B018(16, 4, vars=("Constant",)),
            B018(17, 4, vars=("Constant",)),
            B018(18, 4, vars=("Constant",)),
            B018(19, 4, vars=("Constant",)),
            B018(20, 4, vars=("Constant",)),
            B018(21, 4, vars=("Constant",)),
            B018(22, 4, vars=("List",)),
            B018(23, 4, vars=("Set",)),
            B018(24, 4, vars=("Dict",)),
            B018(28, 4, vars=("Constant",)),
            B018(31, 4, vars=("Constant",)),
            B018(32, 4, vars=("Tuple",)),
            B018(33, 4, vars=("Tuple",)),
        ]

        self.assertEqual(errors, self.errors(*expected))

    def test_b018_classes(self):
        filename = Path(__file__).absolute().parent / "b018_classes.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())

        expected = [
            B018(16, 4, vars=("Constant",)),
            B018(17, 4, vars=("Constant",)),
            B018(18, 4, vars=("Constant",)),
            B018(19, 4, vars=("Constant",)),
            B018(20, 4, vars=("Constant",)),
            B018(21, 4, vars=("Constant",)),
            B018(22, 4, vars=("Constant",)),
            B018(23, 4, vars=("List",)),
            B018(24, 4, vars=("Set",)),
            B018(25, 4, vars=("Dict",)),
            B018(29, 4, vars=("Constant",)),
            B018(32, 4, vars=("Constant",)),
            B018(33, 4, vars=("Tuple",)),
            B018(34, 4, vars=("Tuple",)),
        ]

        self.assertEqual(errors, self.errors(*expected))

    def test_b018_modules(self):
        filename = Path(__file__).absolute().parent / "b018_modules.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())

        expected = [
            B018(9, 0, vars=("Constant",)),
            B018(10, 0, vars=("Constant",)),
            B018(11, 0, vars=("Constant",)),
            B018(12, 0, vars=("Constant",)),
            B018(13, 0, vars=("Constant",)),
            B018(14, 0, vars=("Constant",)),
            B018(15, 0, vars=("Constant",)),
            B018(16, 0, vars=("List",)),
            B018(17, 0, vars=("Set",)),
            B018(18, 0, vars=("Dict",)),
            B018(19, 0, vars=("Tuple",)),
            B018(20, 0, vars=("Tuple",)),
        ]
        self.assertEqual(errors, self.errors(*expected))

    def test_b018_nested(self):
        filename = Path(__file__).absolute().parent / "b018_nested.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())

        expected = [
            B018(3, 0, vars=("Constant",)),
            B018(8, 4, vars=("Constant",)),
            B018(14, 4, vars=("List",)),
            B018(18, 8, vars=("Tuple",)),
            B018(22, 12, vars=("Constant",)),
            B018(25, 16, vars=("Constant",)),
            B018(28, 20, vars=("Set",)),
            B018(31, 20, vars=("Set",)),
            B018(34, 20, vars=("Set",)),
            B018(36, 24, vars=("Constant",)),
            B018(40, 24, vars=("Constant",)),
            B018(42, 24, vars=("Constant",)),
        ]
        self.assertEqual(errors, self.errors(*expected))

    def test_b019(self):
        filename = Path(__file__).absolute().parent / "b019.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B019(61, 5),
                B019(64, 5),
                B019(67, 5),
                B019(70, 5),
                B019(73, 5),
                B019(76, 5),
                B019(79, 5),
                B019(82, 5),
            ),
        )

    def test_b020(self):
        filename = Path(__file__).absolute().parent / "b020.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = [e for e in bbc.run() if e[2][:4] == "B020"]
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
            B023(13, 29, vars=("x",)),
            B023(14, 29, vars=("y",)),
            B023(17, 15, vars=("x",)),
            B023(29, 18, vars=("x",)),
            B023(30, 18, vars=("x",)),
            B023(31, 18, vars=("x",)),
            B023(32, 21, vars=("x",)),
            B023(41, 33, vars=("x",)),
            B023(43, 13, vars=("x",)),
            B023(51, 29, vars=("a",)),
            B023(52, 29, vars=("a_",)),
            B023(53, 29, vars=("b",)),
            B023(54, 29, vars=("c",)),
            B023(62, 16, vars=("j",)),
            B023(62, 20, vars=("k",)),
            B023(69, 9, vars=("l",)),
            B023(114, 23, vars=("x",)),
            B023(115, 26, vars=("x",)),
            B023(116, 36, vars=("x",)),
            B023(117, 37, vars=("x",)),
            B023(118, 36, vars=("x",)),
            B023(169, 28, vars=("name",)),  # known false alarm
            B023(172, 28, vars=("i",)),
        )
        self.assertEqual(errors, expected)

    def test_b024(self):
        filename = Path(__file__).absolute().parent / "b024.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B024(17, 0, vars=("Base_1",)),
            B024(52, 0, vars=("Base_7",)),
            B024(58, 0, vars=("MetaBase_1",)),
            B024(69, 0, vars=("abc_Base_1",)),
            B024(74, 0, vars=("abc_Base_2",)),
        )
        self.assertEqual(errors, expected)

    def test_b025(self):
        filename = Path(__file__).absolute().parent / "b025.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B025(15, 0, vars=("ValueError",)),
                B025(22, 0, vars=("pickle.PickleError",)),
                B025(31, 0, vars=("TypeError",)),
                B025(31, 0, vars=("ValueError",)),
            ),
        )

    def test_b026(self):
        filename = Path(__file__).absolute().parent / "b026.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B026(15, 15),
                B026(16, 15),
                B026(17, 26),
                B026(18, 37),
                B026(19, 15),
                B026(19, 25),
                B026(20, 25),
                B026(21, 19),
            ),
        )

    def test_b027(self):
        filename = Path(__file__).absolute().parent / "b027.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B027(13, 4, vars=("empty_1",)),
            B027(16, 4, vars=("empty_2",)),
            B027(19, 4, vars=("empty_3",)),
            B027(23, 4, vars=("empty_4",)),
            B027(31, 4, vars=("empty_5",)),
        )
        self.assertEqual(errors, expected)

    def test_b028(self):
        filename = Path(__file__).absolute().parent / "b028.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(B028(8, 0), B028(9, 0))
        self.assertEqual(errors, expected)

    def test_b029(self):
        filename = Path(__file__).absolute().parent / "b029.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B029(8, 0),
            B029(13, 0),
        )
        self.assertEqual(errors, expected)

    def test_b030(self):
        filename = Path(__file__).absolute().parent / "b030.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B030(3, 0),
            B030(13, 0),
            B030(18, 0),
        )
        self.assertEqual(errors, expected)

    def test_b031(self):
        filename = Path(__file__).absolute().parent / "b031.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B031(31, 36, vars=("section_items",)),
            B031(35, 30, vars=("section_items",)),
            B031(44, 36, vars=("section_items",)),
        )
        self.assertEqual(errors, expected)

    def test_b032(self):
        filename = Path(__file__).absolute().parent / "b032.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B032(9, 0),
            B032(10, 0),
            B032(12, 0),
            B032(13, 0),
            B032(16, 0),
            B032(17, 0),
            B032(18, 0),
            B032(19, 0),
        )
        self.assertEqual(errors, expected)

    def test_b033(self):
        filename = Path(__file__).absolute().parent / "b033.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B033(6, 17, vars=("3",)),
            B033(7, 23, vars=("'c'",)),
            B033(8, 21, vars=("True",)),
            B033(9, 20, vars=("None",)),
            B033(10, 11, vars=("3.0",)),
            B033(11, 11, vars=("True",)),
            B033(12, 11, vars=("False",)),
            B033(16, 4, vars=("True",)),
            B033(18, 4, vars=("False",)),
        )
        self.assertEqual(errors, expected)

    def test_b034(self):
        filename = Path(__file__).absolute().parent / "b034.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B034(5, 24, vars=("sub", "count")),
            B034(6, 24, vars=("sub", "count")),
            B034(7, 24, vars=("sub", "count")),
            B034(8, 25, vars=("subn", "count")),
            B034(9, 25, vars=("subn", "count")),
            B034(10, 25, vars=("subn", "count")),
            B034(11, 25, vars=("split", "maxsplit")),
            B034(12, 25, vars=("split", "maxsplit")),
            B034(13, 25, vars=("split", "maxsplit")),
        )
        self.assertEqual(errors, expected)

    def test_b035(self):
        filename = Path(__file__).absolute().parent / "b035.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B035(6, 21, vars=("a",)),
            B035(7, 21, vars=(1,)),
            B035(19, 12, vars=("a",)),
            B035(25, 21, vars=("CONST_KEY_VAR",)),
            B035(35, 33, vars=("v3",)),
        )
        self.assertEqual(errors, expected)

    def test_b036(self) -> None:
        filename = Path(__file__).absolute().parent / "b036.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B036(4, 0),
            B036(11, 0),
            B036(20, 0),
            B036(33, 0),
            B036(50, 0),
            B036(58, 0),
        )
        self.assertEqual(errors, expected)

    def test_b037(self) -> None:
        filename = Path(__file__).absolute().parent / "b037.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B037(4, 8),
            B037(11, 12),
            B037(15, 12),
            B037(23, 8),
            B037(29, 8),
            B037(33, 8),
        )
        self.assertEqual(errors, expected)

    def test_b908(self):
        filename = Path(__file__).absolute().parent / "b908.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = self.errors(
            B908(7, 0),
            B908(15, 8),
            B908(21, 8),
            B908(27, 8),
            B017(37, 0),
            B908(37, 0),
            B908(41, 0),
            B908(45, 0),
            B017(56, 0),
        )
        self.assertEqual(errors, expected)

    def test_b907(self):
        filename = Path(__file__).absolute().parent / "b907.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        py39 = sys.version_info >= (3, 9)
        py312 = sys.version_info >= (3, 12)

        def on_py312(number):
            """F-string nodes have column numbers set to 0 on <py312"""
            return number if py312 else 0

        expected = self.errors(
            B907(8, on_py312(9), vars=("var",)),
            B907(9, on_py312(3), vars=("var",)),
            B907(10, on_py312(9), vars=("var",)),
            B907(12, on_py312(9), vars=("var",)),
            B907(13, on_py312(3), vars=("var",)),
            B907(14, on_py312(9), vars=("var",)),
            B907(16, on_py312(5), vars=("'hello'",)),
            B907(17, on_py312(5), vars=("foo()",)),
            # Multiline f-strings have lineno changes as well as colno changes on py312+
            B907(21 if py312 else 20, 7 if py312 else 5, vars=("var",)),
            B907(26 if py312 else 25, 7 if py312 else 5, vars=("var",)),
            B907(31, on_py312(12), vars=("var",)),
            B907(32, on_py312(3), vars=("var",)),
            B907(33, on_py312(3), vars=("var",)),
            B907(33, on_py312(29), vars=("var2",)),
            B907(34, on_py312(3), vars=("var",)),
            B907(34, on_py312(15), vars=("var2",)),
            B907(35, on_py312(3), vars=("var",)),
            B907(35, on_py312(10), vars=("var2",)),
            B907(38, on_py312(13), vars=("var2",)),
            B907(41, on_py312(3), vars=("var",)),
            B907(42, on_py312(3), vars=("var.__str__",)),
            B907(43, on_py312(3), vars=("var.__str__.__repr__",)),
            B907(44, on_py312(3), vars=("3 + 5" if py39 else "BinOp",)),
            B907(45, on_py312(3), vars=("foo()",)),
            B907(46, on_py312(3), vars=("None",)),
            B907(47, on_py312(3), vars=("..." if py39 else "Ellipsis",)),
            B907(48, on_py312(3), vars=("True",)),
            B907(51, on_py312(3), vars=("var",)),
            B907(52, on_py312(3), vars=("var",)),
            B907(53, on_py312(3), vars=("var",)),
            B907(54, on_py312(3), vars=("var",)),
            B907(57, on_py312(3), vars=("var",)),
            B907(60, on_py312(3), vars=("var",)),
            B907(64, on_py312(5), vars=("var",)),
            B907(66, on_py312(3), vars=("var",)),
            B907(68, on_py312(3), vars=("var",)),
        )
        self.assertEqual(errors, expected)

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

    def test_b901(self):
        filename = Path(__file__).absolute().parent / "b901.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B901(8, 8), B901(35, 4)))

    def test_b902(self):
        filename = Path(__file__).absolute().parent / "b902.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B902(22, 17, vars=("'i_am_special'", "instance", "self")),
                B902(24, 30, vars=("'cls'", "instance", "self")),
                B902(26, 4, vars=("(none)", "instance", "self")),
                B902(29, 12, vars=("'self'", "class", "cls")),
                B902(31, 22, vars=("*args", "instance", "self")),
                B902(36, 30, vars=("**kwargs", "instance", "self")),
                B902(38, 32, vars=("*, self", "instance", "self")),
                B902(40, 44, vars=("*, self", "instance", "self")),
                B902(52, 17, vars=("'self'", "metaclass instance", "cls")),
                B902(55, 20, vars=("'cls'", "metaclass class", "metacls")),
            ),
        )

    def test_b902_extended(self):
        filename = Path(__file__).absolute().parent / "b902_extended.py"

        mock_options = Namespace(
            classmethod_decorators=["mylibrary.makeclassmethod", "validator"],
            select=["B902"],
        )
        bbc = BugBearChecker(filename=str(filename), options=mock_options)
        errors = list(bbc.run())

        self.assertEqual(
            errors,
            self.errors(
                B902(5, 22, vars=("'self'", "class", "cls")),
                B902(8, 28, vars=("'self'", "class", "cls")),
                B902(11, 30, vars=("'self'", "class", "cls")),
                B902(14, 27, vars=("'cls'", "instance", "self")),
                B902(18, 13, vars=("'cls'", "instance", "self")),
                B902(22, 13, vars=("'cls'", "instance", "self")),
                B902(26, 13, vars=("'cls'", "instance", "self")),
                B902(30, 13, vars=("'cls'", "instance", "self")),
                # metaclass
                B902(59, 22, vars=("'cls'", "metaclass class", "metacls")),
                B902(62, 28, vars=("'cls'", "metaclass class", "metacls")),
                B902(65, 30, vars=("'cls'", "metaclass class", "metacls")),
                B902(68, 27, vars=("'metacls'", "metaclass instance", "cls")),
                B902(72, 13, vars=("'metacls'", "metaclass instance", "cls")),
                B902(76, 13, vars=("'metacls'", "metaclass instance", "cls")),
                B902(80, 13, vars=("'metacls'", "metaclass instance", "cls")),
                B902(84, 13, vars=("'metacls'", "metaclass instance", "cls")),
            ),
        )

    def test_b902_py38(self):
        filename = Path(__file__).absolute().parent / "b902_py38.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(
            errors,
            self.errors(
                B902(22, 17, vars=("'i_am_special'", "instance", "self")),
                B902(24, 30, vars=("'cls'", "instance", "self")),
                B902(26, 4, vars=("(none)", "instance", "self")),
                B902(29, 12, vars=("'self'", "class", "cls")),
                B902(31, 22, vars=("*args", "instance", "self")),
                B902(36, 30, vars=("**kwargs", "instance", "self")),
                B902(38, 32, vars=("*, self", "instance", "self")),
                B902(40, 44, vars=("*, self", "instance", "self")),
                B902(52, 17, vars=("'self'", "metaclass instance", "cls")),
                B902(55, 20, vars=("'cls'", "metaclass class", "metacls")),
            ),
        )

    def test_b903(self):
        filename = Path(__file__).absolute().parent / "b903.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        self.assertEqual(errors, self.errors(B903(31, 0), B903(37, 0)))

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

    @unittest.skipIf(sys.version_info < (3, 10), "requires 3.10+")
    def test_b905(self):
        filename = Path(__file__).absolute().parent / "b905_py310.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = [
            B905(1, 0),
            B905(2, 0),
            B905(3, 0),
            B905(4, 0),
            B905(4, 15),
            B905(5, 4),
            B905(6, 0),
            B905(21, 0),
            B905(22, 0),
        ]
        self.assertEqual(errors, self.errors(*expected))

    def test_b906(self):
        filename = Path(__file__).absolute().parent / "b906.py"
        bbc = BugBearChecker(filename=str(filename))
        errors = list(bbc.run())
        expected = [
            B906(9, 0),
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
                B950(36, 104, vars=(104, 79)),
                B950(37, 104, vars=(104, 79)),
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
                B950(36, 104, vars=(104, 79)),
                B950(37, 104, vars=(104, 79)),
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
                B950(36, 104, vars=(104, 79)),
                B950(37, 104, vars=(104, 79)),
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

    def test_b909(self):
        filename = Path(__file__).absolute().parent / "b909.py"
        mock_options = Namespace(select=[], extend_select=["B909"])
        bbc = BugBearChecker(filename=str(filename), options=mock_options)
        errors = list(bbc.run())
        expected = [
            B909(12, 4),
            B909(13, 4),
            B909(14, 4),
            B909(15, 4),
            B909(16, 4),
            B909(17, 4),
            B909(18, 4),
            B909(19, 4),
            B909(20, 4),
            B909(21, 4),
            B909(25, 8),
            B909(47, 4),
            B909(48, 4),
            B909(49, 4),
            B909(62, 4),
            B909(63, 4),
            B909(64, 4),
            B909(65, 4),
            B909(66, 4),
            B909(67, 4),
            B909(84, 4),
            B909(85, 4),
            B909(93, 4),
            B909(94, 4),
            B909(95, 4),
            B909(96, 4),
            B909(97, 4),
            B909(102, 4),
            B909(103, 4),
            B909(104, 4),
            B909(105, 4),
            B909(125, 4),
        ]
        self.assertEqual(errors, self.errors(*expected))


class TestFuzz(unittest.TestCase):
    from hypothesis import HealthCheck, given, settings
    from hypothesmith import from_grammar

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
