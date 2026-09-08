# OPTIONS: extend_immutable_calls=["Depends"]
from fastapi import Depends


def this_is_okay_imported(db=Depends(get_db)): ...


def Depends(): ...


def not_okay_redefined(db=Depends(get_db)): ...  # B008: 26
