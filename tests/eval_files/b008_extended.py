# OPTIONS: extend_immutable_calls=["fastapi.Depends", "fastapi.Query"]
from typing import List

import fastapi
import fastapi as fastapi_alias
from fastapi import Depends
from fastapi import Depends as DependsAlias
from fastapi import Depends as loop_depends
from fastapi import Query
from other import Depends as OtherDepends

if condition:
    from fastapi import Depends as conditional_depends


def this_is_okay_extended(db=fastapi.Depends(get_db)): ...


def this_is_okay_extended_second(data: List[str] = fastapi.Query(None)): ...


def this_is_okay_imported(db=Depends(get_db)): ...


def this_is_okay_imported_alias(db=DependsAlias(get_db)): ...


def this_is_okay_module_alias(db=fastapi_alias.Depends(get_db)): ...


class API:
    def this_is_okay_method(self, db=Depends(get_db)): ...


class APIWithRebinding:
    Depends = other

    def not_okay_method(self, db=Depends(get_db)): ...  # B008: 33


class APIWithImportRebinding:
    from other import Depends

    def not_okay_method(self, db=Depends(get_db)): ...  # B008: 33


def not_okay_other_import(db=OtherDepends(get_db)): ...  # B008: 29


Depends: Callable


def this_is_okay_after_annotation_only(db=Depends(get_db)): ...


def Depends(): ...


def not_okay_redefined(db=Depends(get_db)): ...  # B008: 26


Query = lambda value: value


def not_okay_reassigned(data: List[str] = Query(None)): ...  # B008: 42


def not_okay_conditional_import(
    db=conditional_depends(get_db),  # B008: 7
): ...


for loop_depends in providers:
    _ = loop_depends


def not_okay_loop_rebound(db=loop_depends(get_db)): ...  # B008: 29


from fastapi import Depends as walrus_depends


def not_okay_walrus_default(
    first=(walrus_depends := other),
    db=walrus_depends(get_db),  # B008: 7
): ...


from fastapi import Depends as decorator_depends


@decorate((decorator_depends := other))
def not_okay_walrus_decorator(db=decorator_depends(get_db)): ...  # B008: 33


from fastapi import Depends as class_base_depends


class RebindsInBase((class_base_depends := OtherBase)): ...


def not_okay_walrus_class_base(db=class_base_depends(get_db)): ...  # B008: 34


from fastapi import Depends as class_keyword_depends


class RebindsInKeyword(metaclass=(class_keyword_depends := Meta)): ...


def not_okay_walrus_class_keyword(
    db=class_keyword_depends(get_db),  # B008: 7
): ...


from fastapi import Depends as nested_comprehension_depends

_ = [
    [(nested_comprehension_depends := other) for inner in values]
    for outer in values
]


def not_okay_walrus_nested_comprehension(
    db=nested_comprehension_depends(get_db),  # B008: 7
): ...


from fastapi import Depends as lambda_default_depends


@decorate(lambda value=(lambda_default_depends := other): value)
def not_okay_walrus_lambda_default(
    db=lambda_default_depends(get_db),  # B008: 7
): ...


from fastapi import Depends as function_lambda_depends


def not_okay_walrus_function_lambda_default(
    first=(lambda value=(function_lambda_depends := other): value),
    db=function_lambda_depends(get_db),  # B008: 7
): ...


from fastapi import Depends as annotation_depends


def annotation_rebinds_import(value: (annotation_depends := other)): ...


def not_okay_walrus_annotation(
    db=annotation_depends(get_db),  # B008: 7
): ...


from fastapi import Depends as generator_depends

_ = ((generator_depends := other) for value in values)


def this_is_okay_deferred_generator(db=generator_depends(get_db)): ...


from fastapi import Depends as default_generator_depends


def this_is_okay_deferred_default_generator(
    generator=((default_generator_depends := other) for value in values),
    db=default_generator_depends(get_db),
): ...


from fastapi import Depends as decorator_generator_depends


@decorate((decorator_generator_depends := other) for value in values)
def this_is_okay_deferred_decorator_generator(
    db=decorator_generator_depends(get_db),
): ...


from fastapi import Depends as global_depends


class GlobalRebinding:
    global global_depends
    global_depends = other


def not_okay_class_global_rebinding(
    db=global_depends(get_db),  # B008: 7
): ...


from fastapi import Depends as global_def_depends


class GlobalDefRebinding:
    global global_def_depends

    @staticmethod
    def global_def_depends(): ...


def not_okay_class_global_def(
    db=global_def_depends(get_db),  # B008: 7
): ...


from fastapi import Depends as global_import_depends


class GlobalImportRebinding:
    global global_import_depends
    from other import Depends as global_import_depends


def not_okay_class_global_import(
    db=global_import_depends(get_db),  # B008: 7
): ...
