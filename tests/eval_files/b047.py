import os

try:
    pass
except BaseException:
    raise
except Exception:  # B047: 0, "Exception", "BaseException", ""
    pass

try:
    pass
except BaseException:
    raise
except:  # B001: 0 # B047: 0, "BaseException", "BaseException", ""
    pass

try:
    pass
except Exception:
    pass
except ValueError:  # B047: 0, "ValueError", "Exception", ""
    pass
except (KeyError, MyError):  # B047: 0, "KeyError", "Exception", ""
    pass
except KeyboardInterrupt:
    pass

try:
    pass
except (TypeError, LookupError) as e:
    pass
except IndexError as e:  # B047: 0, "IndexError", "LookupError", ""
    pass
except (KeyError, UnicodeDecodeError):  # B047: 0, "KeyError", "LookupError", ""
    pass

# IOError is an alias of OSError
try:
    pass
except OSError:
    pass
except IOError:  # B047: 0, "IOError", "OSError", ""
    pass

# starred tuples are expanded
try:
    pass
except Exception:
    pass
except (*(ValueError,),):  # B013: 0, "ValueError", "" # B047: 0, "ValueError", "Exception", ""
    pass

# good
try:
    pass
except ValueError:
    pass
except Exception:
    pass
except BaseException:
    raise

try:
    pass
except KeyError:
    pass
except IndexError:
    pass
except LookupError:
    pass

# not builtins, so the hierarchy is unknown
try:
    pass
except MyError:
    pass
except MySubError:
    pass

try:
    pass
except os.error:
    pass
except FileNotFoundError:
    pass

# the same exception caught twice is B025
try:  # B025: 0, "ValueError"
    pass
except ValueError:
    pass
except ValueError:
    pass
