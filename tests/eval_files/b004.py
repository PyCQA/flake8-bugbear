def this_is_a_bug():
    o = object()
    if hasattr(o, "__call__"):  # B004: 7
        print("Ooh, callable! Or is it?")
    if getattr(o, "__call__", False):  # B004: 7
        print("Ooh, callable! Or is it?")


def this_is_fine():
    o = object()
    if callable(o):
        print("Ooh, this is actually callable.")
