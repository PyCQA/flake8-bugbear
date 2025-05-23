# OPTIONS: classmethod_decorators=["mylibrary.makeclassmethod", "validator"], select=["B902"]
class Errors:
    # correctly registered as classmethod
    @validator
    def foo_validator(self) -> None: ... # B902: 22, "'self'", "class", "cls"

    @other.validator
    def foo_other_validator(self) -> None: ... # B902: 28, "'self'", "class", "cls"

    @foo.bar.validator
    def foo_foo_bar_validator(self) -> None: ... # B902: 30, "'self'", "class", "cls"

    @validator.blah
    def foo_validator_blah(cls) -> None: ... # B902: 27, "'cls'", "instance", "self"

    # specifying attribute in options is not valid
    @mylibrary.makeclassmethod
    def foo2(cls) -> None: ... # B902: 13, "'cls'", "instance", "self"

    # specified attribute in options
    @makeclassmethod
    def foo6(cls) -> None: ... # B902: 13, "'cls'", "instance", "self"

    # classmethod is default, but if not specified it's ignored
    @classmethod
    def foo3(cls) -> None: ... # B902: 13, "'cls'", "instance", "self"

    # random unknown decorator
    @aoeuaoeu
    def foo5(cls) -> None: ... # B902: 13, "'cls'", "instance", "self"


class NoErrors:
    @validator
    def foo1(cls) -> None: ...

    @other.validator
    def foo4(cls) -> None: ...

    @mylibrary.makeclassmethod
    def foo2(self) -> None: ...

    @classmethod
    def foo3(self) -> None: ...

    @aoeuaoeu
    def foo5(self) -> None: ...

    @makeclassmethod
    def foo6(self) -> None: ...


# Above tests, duplicated to check that the separate logic for metaclasses also works


class ErrorsMeta(type):
    # correctly registered as classmethod
    @validator
    def foo_validator(cls) -> None: ... # B902: 22, "'cls'", "metaclass class", "metacls"

    @other.validator
    def foo_other_validator(cls) -> None: ... # B902: 28, "'cls'", "metaclass class", "metacls"

    @foo.bar.validator
    def foo_foo_bar_validator(cls) -> None: ... # B902: 30, "'cls'", "metaclass class", "metacls"

    @validator.blah
    def foo_validator_blah(metacls) -> None: ... # B902: 27, "'metacls'", "metaclass instance", "cls"

    # specifying attribute in options is not valid
    @mylibrary.makeclassmethod
    def foo2(metacls) -> None: ... # B902: 13, "'metacls'", "metaclass instance", "cls"

    # specified attribute in options
    @makeclassmethod
    def foo6(metacls) -> None: ... # B902: 13, "'metacls'", "metaclass instance", "cls"

    # classmethod is default, but if not specified it's ignored
    @classmethod
    def foo3(metacls) -> None: ... # B902: 13, "'metacls'", "metaclass instance", "cls"

    # random unknown decorator
    @aoeuaoeu
    def foo5(metacls) -> None: ... # B902: 13, "'metacls'", "metaclass instance", "cls"


class NoErrorsMeta(type):
    @validator
    def foo1(metacls) -> None: ...

    @other.validator
    def foo4(metacls) -> None: ...

    @mylibrary.makeclassmethod
    def foo2(cls) -> None: ...

    @classmethod
    def foo3(cls) -> None: ...

    @aoeuaoeu
    def foo5(cls) -> None: ...

    @makeclassmethod
    def foo6(cls) -> None: ...
