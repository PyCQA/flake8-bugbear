# Python 3.15 allows dict unpacking in dict comprehensions. There is no
# key in that case, only an unpacked expression, so B035 must stay quiet.

unpack_ok = {**base for _ in range(3)}
unpack_key_name_ok = {**d for d in dicts}

# Static keys are still reported.
static_key_str = {"a": i for i in range(3)}  # B035: 18, "a"
static_key_int = {1: i for i in range(3)}  # B035: 18, 1
