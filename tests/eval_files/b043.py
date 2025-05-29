# Valid usage
attr_name = "name"
delattr(obj, attr_name)
for field in fields_to_remove:
    delattr(obj, field)
delattr(obj, some_name())
delattr(obj, f"field_{index}")

# Invalid usage
delattr(obj, "name")  # B043: 0
delattr(obj, r"raw_attr")  # B043: 0