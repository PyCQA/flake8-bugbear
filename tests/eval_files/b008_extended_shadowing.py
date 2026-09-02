# OPTIONS: extend_immutable_calls=["Depends", "factory"]
from fastapi import Depends


def this_is_okay_imported(db=Depends(get_db)): ...


def Depends(): ...


def not_okay_redefined(db=Depends(get_db)): ...  # B008: 26


def source_path_stays_configured(
    first=(factory := other), second=factory()
): ...
