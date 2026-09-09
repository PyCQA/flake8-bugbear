haystack = "hello world"
needle = "world"


# Bad: the index is used directly as a boolean.
if haystack.find(needle):  # B044: 3
    pass

if not haystack.find(needle):  # B044: 7
    pass

while haystack.find(needle):  # B044: 6
    pass

assert haystack.find(needle)  # B044: 7

found = "yes" if haystack.find(needle) else "no"  # B044: 17

if haystack.find(needle) and needle:  # B044: 3
    pass

if needle or haystack.find(needle):  # B044: 13
    pass

if not (haystack.find(needle) or needle):  # B044: 8
    pass

matches = [c for c in haystack if haystack.find(c)]  # B044: 34

if haystack.rfind(needle):  # B044: 3
    pass

if b"data".find(b"a"):  # B044: 3
    pass


# OK: the returned index is compared explicitly.
if haystack.find(needle) == 0:
    pass

if haystack.find(needle) != -1:
    pass

if haystack.find(needle) >= 0:
    pass

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
