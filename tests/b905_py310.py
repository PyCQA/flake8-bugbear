zip()
zip(range(3))
zip("a", "b")
zip("a", "b", *zip("c"))
zip(zip("a"), strict=False)
zip(zip("a", strict=True))

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

zip([1, 2, 3], itertools.repeat(1, 1))
zip([1, 2, 3], itertools.repeat(1, times=4))
