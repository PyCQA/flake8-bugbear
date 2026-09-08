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
