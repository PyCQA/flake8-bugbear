try:
    import something
except:  # B001: 0
    # should be except ImportError:
    import something_else as something

try:
    pass
except ValueError:
    # no warning here, all good
    pass

try:
    pass
except (KeyError, IndexError):
    # no warning here, all good
    pass

try:
    pass
except ValueError as be:
    # no warning here, all good
    pass

try:
    pass
except IndexError:
    # no warning here, all good
    pass


def func(**kwargs):
    try:
        is_debug = kwargs["debug"]
    except:  # B001: 4
        # should be except KeyError:
        return
