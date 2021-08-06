"""
Should emit:
B009 - Line 17, 18, 19
B010 - Line 28, 29, 30
"""

# Valid getattr usage
getattr(foo, bar)
getattr(foo, "bar", None)
getattr(foo, "bar{foo}".format(foo="a"), None)
getattr(foo, "bar{foo}".format(foo="a"))
getattr(foo, bar, None)
getattr(foo, "123abc")
getattr(foo, "except")

# Invalid usage
getattr(foo, "bar")
getattr(foo, "_123abc")
getattr(foo, "abc123")

# Valid setattr usage
setattr(foo, bar, None)
setattr(foo, "bar{foo}".format(foo="a"), None)
setattr(foo, "123abc", None)
setattr(foo, "except", None)

# Invalid usage
setattr(foo, "bar", None)
setattr(foo, "_123abc", None)
setattr(foo, "abc123", None)
