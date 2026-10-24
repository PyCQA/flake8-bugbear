_ = zip() # B905: 4
_ = zip(range(3)) # B905: 4
_ = zip("a", "b") # B905: 4
_ = zip("a", "b", *zip("c")) # B905: 4 # B905: 19
_ = zip(zip("a"), strict=False) # B905: 8
_ = zip(zip("a", strict=True)) # B905: 4

_ = zip(range(3), strict=True)
_ = zip("a", "b", strict=False)
_ = zip("a", "b", "c", strict=True)

# infinite iterators from itertools module should not raise errors
import itertools

_ = zip([1, 2, 3], itertools.cycle("ABCDEF"))
_ = zip([1, 2, 3], itertools.count())
_ = zip([1, 2, 3], itertools.repeat(1))
_ = zip([1, 2, 3], itertools.repeat(1, None))
_ = zip([1, 2, 3], itertools.repeat(1, times=None))

_ = zip([1, 2, 3], itertools.repeat(1, 1)) # B905: 4
_ = zip([1, 2, 3], itertools.repeat(1, times=4)) # B905: 4
