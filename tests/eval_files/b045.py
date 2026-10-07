for i in xs:
    for i in ys:  # B045: 8, "i"
        print(i)
    print(i)


async def check():
    async for value in xs:
        async for value in ys:  # B045: 18, "value"
            print(value)
        print(value)
