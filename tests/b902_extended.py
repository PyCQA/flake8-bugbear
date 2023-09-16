# parameters: --classmethod-decorators=["mylibrary.classmethod", "validator"]
class Errors:
    # correctly registered as classmethod
    @validator
    def foo_validator(self) -> None: ...

    @other.validator
    def foo_other_validator(self) -> None: ...

    @foo.bar.validator
    def foo_foo_bar_validator(self) -> None: ...

    @validator.blah
    def foo_validator_blah(cls) -> None: ...

    # specifying attribute in options is not valid
    @mylibrary.makeclassmethod
    def foo2(cls) -> None: ...

    # specified attribute in options
    @makeclassmethod
    def foo6(cls) -> None: ...

    # classmethod is default, but if not specified it's ignored
    @classmethod
    def foo3(cls) -> None: ...

    # random unknown decorator
    @aoeuaoeu
    def foo5(cls) -> None: ...


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
    def foo_validator(cls) -> None: ...

    @other.validator
    def foo_other_validator(cls) -> None: ...

    @foo.bar.validator
    def foo_foo_bar_validator(cls) -> None: ...

    @validator.blah
    def foo_validator_blah(metacls) -> None: ...

    # specifying attribute in options is not valid
    @mylibrary.makeclassmethod
    def foo2(metacls) -> None: ...

    # specified attribute in options
    @makeclassmethod
    def foo6(metacls) -> None: ...

    # classmethod is default, but if not specified it's ignored
    @classmethod
    def foo3(metacls) -> None: ...

    # random unknown decorator
    @aoeuaoeu
    def foo5(metacls) -> None: ...


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
