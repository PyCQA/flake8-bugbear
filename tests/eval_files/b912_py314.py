map(lambda x: x, "a", "b")  # B912: 0
map(lambda x: x, "a", "b", *map("c"))  # B912: 0
map(lambda x: x, "a", map(lambda x: x, "a"), strict=True)  # B912: 22

map()
map(lambda x: x, "a")
map(lambda x: x, "a", "b", strict=False)
map(lambda x: x, "a", "b", "c", strict=True)
