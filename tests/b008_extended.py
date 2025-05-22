# OPTIONS: extend_immutable_calls=["fastapi.Depends", "fastapi.Query"]
from typing import List

import fastapi
from fastapi import Query


def this_is_okay_extended(db=fastapi.Depends(get_db)): ...


def this_is_okay_extended_second(data: List[str] = fastapi.Query(None)): ...


# not okay, relative import not listed
def not_okay(data: List[str] = Query(None)): ...  # B008: 31
