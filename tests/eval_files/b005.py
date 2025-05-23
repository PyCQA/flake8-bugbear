s = "qwe"
s.strip(s)
s.strip("we")
s.strip(".facebook.com")  # B005: 0
s.strip("e")
s.strip("\n\t ")
s.strip(r"\n\t ")  # B005: 0
s.lstrip(s)
s.lstrip("we")
s.lstrip(".facebook.com")  # B005: 0
s.lstrip("e")
s.lstrip("\n\t ")
s.lstrip(r"\n\t ")  # B005: 0
s.rstrip(s)
s.rstrip("we")
s.rstrip(".facebook.com")  # B005: 0
s.rstrip("e")
s.rstrip("\n\t ")
s.rstrip(r"\n\t ")  # B005: 0

from somewhere import other_type, strip

strip("we")
other_type().lstrip()
other_type().rstrip(["a", "b", "c"])
other_type().strip("a", "b")

import test, test2  # isort: skip
import test_as as test3

test.strip("test")
test2.strip("test")
test3.strip("test")
