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
