"""
Should emit:
B014 - on lines 11, 17, 28, 42, 49, 56, and 74.
"""

import binascii
import re

try:
    pass
except (Exception, TypeError):  # B014: 0, "Exception, TypeError", "", "Exception", ""
    # TypeError is a subclass of Exception, so it doesn't add anything
    pass

try:
    pass
except (OSError, OSError) as err:  # B014: 0, "OSError, OSError", " as err", "OSError", ""
    # Duplicate exception types are useless
    pass


class MyError(Exception):
    pass


try:
    pass
except (MyError, MyError):  # B014: 0, "MyError, MyError", "", "MyError", ""
    # Detect duplicate non-builtin errors
    pass


try:
    pass
except (MyError, Exception) as e:
    # Don't assume that we're all subclasses of Exception
    pass


try:
    pass
except (MyError, BaseException) as e:  # B014: 0, "MyError, BaseException", " as e", "BaseException", ""
    # But we *can* assume that everything is a subclass of BaseException
    raise e


try:
    pass
except (re.error, re.error):  # B014: 0, "re.error, re.error", "", "re.error", ""
    # Duplicate exception types as attributes
    pass


try:
    pass
except (IOError, EnvironmentError, OSError):  # B014: 0, "IOError, EnvironmentError, OSError", "", "OSError", ""
    # Detect if a primary exception and any its aliases are present.
    #
    # Since Python 3.3, IOError, EnvironmentError, WindowsError, mmap.error,
    # socket.error and select.error are aliases of OSError. See PEP 3151 for
    # more info.
    pass


try:
    pass
except (MyException, NotImplemented):
    # NotImplemented is not an exception, let's not crash on it.
    pass


try:
    pass
except (ValueError, binascii.Error):  # B014: 0, "ValueError, binascii.Error", "", "ValueError", ""
    # binascii.Error is a subclass of ValueError.
    pass
