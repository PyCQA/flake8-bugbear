import contextvars
import time
from contextvars import ContextVar

ContextVar("cv", default=[])  # bad
ContextVar("cv", default=list())  # bad
ContextVar("cv", default=set())  # bad
ContextVar("cv", default=time.time())  # bad (B008-like)
contextvars.ContextVar("cv", default=[])  # bad


# good
ContextVar("cv", default=())
contextvars.ContextVar("cv", default=())
ContextVar("cv", default=tuple())

# see tests/b006_b008.py for more comprehensive tests
