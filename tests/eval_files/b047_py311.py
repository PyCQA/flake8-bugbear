try:
    pass
except* Exception:
    pass
except* ValueError:  # B047: 0, "ValueError", "Exception", "*"
    pass

try:
    pass
except* (TypeError, OSError):
    pass
except* (FileNotFoundError, ValueError):  # B047: 0, "FileNotFoundError", "OSError", "*"
    pass
