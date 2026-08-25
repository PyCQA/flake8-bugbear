haystack = "hello world"
needle = "world"


# Bad: the index is used directly as a boolean.
if haystack.find(needle):  # B048: 3
    pass

if not haystack.find(needle):  # B048: 7
    pass

while haystack.find(needle):  # B048: 6
    pass

assert haystack.find(needle)  # B048: 7

found = "yes" if haystack.find(needle) else "no"  # B048: 17

if haystack.find(needle) and needle:  # B048: 3
    pass

if needle or haystack.find(needle):  # B048: 13
    pass

if not (haystack.find(needle) or needle):  # B048: 8
    pass

matches = [c for c in haystack if haystack.find(c)]  # B048: 34

if haystack.rfind(needle):  # B048: 3
    pass

if b"data".find(b"a"):  # B048: 3
    pass


if (pos := haystack.find(needle)):  # B048: 11
    pass

while (pos := haystack.rfind(needle)):  # B048: 14
    pass

fallback = haystack.find(needle) or -1  # B048: 11

negated = not haystack.find(needle)  # B048: 14

if haystack.find(sub=needle):  # B048: 3
    pass


# OK: the returned index is compared explicitly.
if haystack.find(needle) == 0:
    pass

if haystack.find(needle) != -1:
    pass

if haystack.find(needle) >= 0:
    pass

if (pos := haystack.find(needle)) != -1:
    pass

if bool(haystack.find(needle)):
    pass


# Out of scope: B048 only checks the `.find()`/`.rfind()` call itself.
# Testing a variable that holds the index is the same truthiness pitfall,
# but the call is no longer visible at the test, so it is not reported.
index = haystack.find(needle)
if index:
    pass


def get_index():
    return haystack.find(needle)


haystack.find(needle)
print(haystack.find(needle))

# OK: `.index()` raises instead of returning -1, and unrelated `.find()` users
# such as BeautifulSoup are not our concern here, but a plain attribute is.
if haystack.index(needle):
    pass
