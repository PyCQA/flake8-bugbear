import re
from re import sub

# error
re.sub("a", "b", "aaa", re.IGNORECASE) # B034: 24, "sub", "count"
re.sub("a", "b", "aaa", 5) # B034: 24, "sub", "count"
re.sub("a", "b", "aaa", 5, re.IGNORECASE) # B034: 24, "sub", "count"
re.subn("a", "b", "aaa", re.IGNORECASE) # B034: 25, "subn", "count"
re.subn("a", "b", "aaa", 5) # B034: 25, "subn", "count"
re.subn("a", "b", "aaa", 5, re.IGNORECASE) # B034: 25, "subn", "count"
re.split(" ", "a a a a", re.I) # B034: 25, "split", "maxsplit"
re.split(" ", "a a a a", 2) # B034: 25, "split", "maxsplit"
re.split(" ", "a a a a", 2, re.I) # B034: 25, "split", "maxsplit"

# okay
re.sub("a", "b", "aaa")
re.sub("a", "b", "aaa", flags=re.IGNORECASE)
re.sub("a", "b", "aaa", count=5)
re.sub("a", "b", "aaa", count=5, flags=re.IGNORECASE)
re.subn("a", "b", "aaa")
re.subn("a", "b", "aaa", flags=re.IGNORECASE)
re.subn("a", "b", "aaa", count=5)
re.subn("a", "b", "aaa", count=5, flags=re.IGNORECASE)
re.split(" ", "a a a a", flags=re.I)
re.split(" ", "a a a a", maxsplit=2)
re.split(" ", "a a a a", maxsplit=2, flags=re.I)


# not covered
sub("a", "b", "aaa", re.IGNORECASE)
