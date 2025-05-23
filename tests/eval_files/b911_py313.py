import itertools
from itertools import batched

# Expect B911
batched(range(3), 2) # B911: 0
batched(range(3), n=2) # B911: 0
batched(iterable=range(3), n=2) # B911: 0
itertools.batched(range(3), 2) # B911: 0
itertools.batched(range(3), n=2) # B911: 0
itertools.batched(iterable=range(3), n=2) # B911: 0

# OK
batched(range(3), 2, strict=True)
batched(range(3), n=2, strict=True)
batched(iterable=range(3), n=2, strict=True)
batched(range(3), 2, strict=False)
batched(range(3), n=2, strict=False)
batched(iterable=range(3), n=2, strict=False)
itertools.batched(range(3), 2, strict=True)
itertools.batched(range(3), n=2, strict=True)
itertools.batched(iterable=range(3), n=2, strict=True)
itertools.batched(range(3), 2, strict=False)
itertools.batched(range(3), n=2, strict=False)
itertools.batched(iterable=range(3), n=2, strict=False)
