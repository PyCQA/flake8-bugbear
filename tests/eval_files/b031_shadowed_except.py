"""
Should emit:
B031 - on line 30
"""

# An except target named groupby is not itertools.groupby (#356).
import itertools


class CallableError(Exception):
    def __call__(self, x, y):
        return dict().items()


try:
    raise CallableError
except CallableError as groupby:
    for _, v in groupby(None, None):
        if v:
            pass
        if v:
            pass


for _, v in itertools.groupby(None, None):
    if v:
        pass
    if v:  # B031: 7, "v"
        pass
