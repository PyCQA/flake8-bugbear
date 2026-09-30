# OPTIONS: extend_immutable_calls=["factory"]
from contextvars import ContextVar

ContextVar("configured", default=((factory := other), factory())[1])
ContextVar("not_configured", default=other())  # B039: 37
