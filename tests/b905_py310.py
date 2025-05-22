zip() # B905: 0
zip(range(3)) # B905: 0
zip("a", "b") # B905: 0
zip("a", "b", *zip("c")) # B905: 0 # B905: 15
zip(zip("a"), strict=False) # B905: 4
zip(zip("a", strict=True)) # B905: 0

zip(range(3), strict=True)
zip("a", "b", strict=False)
zip("a", "b", "c", strict=True)

# infinite iterators from itertools module should not raise errors
import itertools

zip([1, 2, 3], itertools.cycle("ABCDEF"))
zip([1, 2, 3], itertools.count())
zip([1, 2, 3], itertools.repeat(1))
zip([1, 2, 3], itertools.repeat(1, None))
zip([1, 2, 3], itertools.repeat(1, times=None))

zip([1, 2, 3], itertools.repeat(1, 1)) # B905: 0
zip([1, 2, 3], itertools.repeat(1, times=4)) # B905: 0
