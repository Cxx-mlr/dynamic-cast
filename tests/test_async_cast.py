from dynamic_cast import async_cast

@async_cast
async def sum(a: int, b: int) -> int:
    return a + b

async def test_sum():
    assert await sum("28", "28") == 56