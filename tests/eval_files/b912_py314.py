_ = map(lambda x: x, "a", "b")  # B912: 4
_ = map(lambda x: x, "a", "b", *map("c"))  # B912: 4
_ = map(lambda x: x, "a", map(lambda x: x, "a"), strict=True)

_ = map()
_ = map(lambda x: x, "a")
_ = map(lambda x: x, "a", "b", strict=False)
_ = map(lambda x: x, "a", "b", "c", strict=True)
