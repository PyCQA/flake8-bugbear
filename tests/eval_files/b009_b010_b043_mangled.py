class Foo:
    __slots__ = ("__bar",)

    getattr(foo, "__bar")

    def get(self):
        return getattr(self, "__bar")

    def set(self, value):
        setattr(self, "__bar", value)

    def delete(self):
        delattr(self, "__bar")

    def nested(self):
        def inner():
            return getattr(self, "__bar")

        return inner

    def dunder(self):
        getattr(self, "__dict__")  # B009: 8
        setattr(self, "__doc__", None)  # B010: 8
        delattr(self, "__doc__")  # B043: 8

    def single_underscore(self):
        getattr(self, "_bar")  # B009: 8


getattr(foo, "__bar")  # B009: 0
setattr(foo, "__bar", None)  # B010: 0
delattr(foo, "__bar")  # B043: 0


def outside(obj):
    return getattr(obj, "__bar")  # B009: 11
