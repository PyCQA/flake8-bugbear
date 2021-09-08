"""
Should emit:
B904 - on lines 10, 11 and 16
"""

try:
    raise ValueError
except ValueError:
    if "abc":
        raise TypeError
    raise UserWarning
except AssertionError:
    raise  # Bare `raise` should not be an error
except Exception as err:
    assert err
    raise Exception("No cause here...")
except BaseException as base_err:
    # Might use this instead of bare raise with the `.with_traceback()` method
    raise base_err
finally:
    raise Exception("Nothing to chain from, so no warning here")
