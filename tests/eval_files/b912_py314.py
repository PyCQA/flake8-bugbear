map()  # B912: 0
map(range(3))  # B912: 0
map("a", "b")  # B912: 0
map("a", "b", *map("c"))  # B912: 0 # B912: 15
map(map("a"), strict=False)  # B912: 4
map(map("a", strict=True))  # B912: 0

map(range(3), strict=True)
map("a", "b", strict=False)
map("a", "b", "c", strict=True)
