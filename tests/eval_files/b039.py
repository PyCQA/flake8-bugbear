import contextvars
import time
from contextvars import ContextVar

ContextVar("cv", default=[])  # bad # B039: 25
ContextVar("cv", default=list())  # bad # B039: 25
ContextVar("cv", default=set())  # bad # B039: 25
ContextVar("cv", default=time.time())  # bad (B008-like) # B039: 25
contextvars.ContextVar("cv", default=[])  # bad # B039: 37


# good
ContextVar("cv", default=())
contextvars.ContextVar("cv", default=())
ContextVar("cv", default=tuple())

# see tests/b006_b008.py for more comprehensive tests
