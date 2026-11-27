"""
Should emit:
B905 - on lines 20, 21
"""

# count(), cycle() and repeat() imported from itertools under another name are
# infinite.
from itertools import count as c
from itertools import cycle as cyc
from itertools import repeat as rep

from mylib import count as mc

_ = zip([1, 2, 3], c())
_ = zip([1, 2, 3], cyc("ABCDEF"))
_ = zip([1, 2, 3], rep(1))
_ = zip([1, 2, 3], rep(1, None))
_ = zip([1, 2, 3], rep(1, times=None))

_ = zip([1, 2, 3], rep(1, 1))  # B905: 4
_ = zip([1, 2, 3], mc())  # B905: 4
