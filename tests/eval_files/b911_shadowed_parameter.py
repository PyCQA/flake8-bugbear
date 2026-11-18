"""
Should emit:
B911 - on line 15
"""

# A parameter named batched is not itertools.batched.
import itertools


def chunks(items, batched):
    for chunk in batched(items, 10):
        print(chunk)


itertools.batched(range(3), 2)  # B911: 0
