"""
Should emit:
B032 - on lines 9, 10, 12, 13, 16-19
"""

# Flag these
dct = {"a": 1}

dct["b"]: 2 # B032: 0
dct.b: 2 # B032: 0

dct["b"]: "test" # B032: 0
dct.b: "test" # B032: 0

test = "test"
dct["b"]: test # B032: 0
dct["b"]: test.lower() # B032: 0
dct.b: test # B032: 0
dct.b: test.lower() # B032: 0

# Do not flag below
typed_dct: dict[str, int] = {"a": 1}
typed_dct["b"] = 2
typed_dct.b = 2


class TestClass:
    def test_self(self):
        self.test: int
