# OK - consts in regular dict
regular_dict = {"a": 1, "b": 2}
regular_nested_dict = {"a": 1, "nested": {"b": 2, "c": "three"}}

# bad - const key in dict comprehension
bad_const_key_str = {"a": i for i in range(3)}
bad_const_key_int = {1: i for i in range(3)}

# OK - const value in dict comp
const_val = {i: "a" for i in range(3)}

# OK - expression with const in dict comp
key_expr_with_const = {i * i: i for i in range(3)}
key_expr_with_const2 = {"a" * i: i for i in range(3)}

# nested
nested_bad_and_good = {
    "good": {"a": 1, "b": 2},
    "bad": {"a": i for i in range(3)},
}

CONST_KEY_VAR = "KEY"

# bad
bad_const_key_var = {CONST_KEY_VAR: i for i in range(3)}

# OK - variable from tuple
var_from_tuple = {k: v for k, v in {}.items()}

# OK - variable from nested tuple
var_from_nested_tuple = {v2: k for k, (v1, v2) in {"a": (1, 2)}.items()}

# bad - variabe not from generator
v3 = 1
bad_var_not_from_nested_tuple = {v3: k for k, (v1, v2) in {"a": (1, 2)}.items()}

# OK - variable from named expression
var_from_named_expr = {
    k: v
    for v in {"key": "foo", "data": {}}
    if (k := v.get("key")) is not None
}

# nested generators with named expressions
var_from_named_expr_nested = {
    k: v
    for v in {"keys": [{"key": "foo"}], "data": {}}
    if (keys := v.get("keys")) is not None
    for item in keys
    if (k := item.get("key")) is not None
}
