from dynamic_cast import dynamic_cast

@dynamic_cast
def sum(a: int, b: int) -> int:
    return a + b

def test_sum():
    assert sum("28", "28") == 56