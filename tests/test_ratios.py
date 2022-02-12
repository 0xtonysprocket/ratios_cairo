import pytest
import math
from hypothesis import given, strategies as st, settings

# from OZ utils.py
def to_uint(a):
    """Takes in value, returns uint256-ish tuple."""
    return (a & ((1 << 128) - 1), a >> 128)


def from_uint(uint):
    """Takes in uint256-ish tuple, returns value."""
    return uint[0] + (uint[1] << 128)


"""
@given(
    x=st.integers(min_value=1, max_value=100000),
    y=st.integers(min_value=1, max_value=100000),
    z=st.integers(min_value=1, max_value=100000),
    k=st.integers(min_value=1, max_value=100000),
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_ratio_diff(ratio_factory, x, y, z, k):
    ratio = ratio_factory

    base = (to_uint(x), to_uint(y))  # x/y
    other = (to_uint(z), to_uint(k))  # z/k

    root = await ratio.ratio_diff(base, other).call()
    assert (from_uint(root.result[0][0]), from_uint(root.result[0][1])) == (
        (
            abs(z * y - x * k),
            k * y,
        )
        if k != y
        else (abs(z - x), k)
    )


@given(
    x=st.integers(min_value=1, max_value=100000),
    y=st.integers(min_value=1, max_value=100000),
    z=st.integers(min_value=1, max_value=100000),
    k=st.integers(min_value=1, max_value=100000),
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_ratio_le_eq(ratio_factory, x, y, z, k):
    ratio = ratio_factory

    base = (to_uint(x), to_uint(y))  # x/y
    other = (to_uint(z), to_uint(k))  # z/k

    root = await ratio.ratio_less_than_or_eq(base, other).call()
    print(root.result)
    print(root.result[0])
    assert root.result[0] == (1 if x / y <= z / k else 0)


@given(
    x=st.integers(min_value=1, max_value=100000),
    y=st.integers(min_value=1, max_value=100000),
    z=st.integers(min_value=1, max_value=100000),
    k=st.integers(min_value=1, max_value=100000),
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_ratio_mul(ratio_factory, x, y, z, k):
    ratio = ratio_factory

    base = (to_uint(x), to_uint(y))  # x/y
    other = (to_uint(z), to_uint(k))  # exponent

    root = await ratio.ratio_mul(base, other).call()
    assert (from_uint(root.result[0][0]), from_uint(root.result[0][1])) == (
        x * z,
        y * k,
    )


@given(
    x=st.integers(min_value=1, max_value=100),
    y=st.integers(min_value=1, max_value=100),
    z=st.integers(min_value=1, max_value=9),
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_ratio_pow(ratio_factory, x, y, z):
    ratio = ratio_factory

    base = (to_uint(x), to_uint(y))  # x/y
    power = to_uint(z)  # exponent

    root = await ratio.ratio_pow(base, power).call()
    assert (from_uint(root.result[0][0]), from_uint(root.result[0][1])) == (
        x ** z,
        y ** z,
    )
"""

"""
@given(
    x=st.integers(min_value=1, max_value=100000),
    y=st.integers(min_value=1, max_value=100000),
    z=st.integers(min_value=1, max_value=100000),
    k=st.integers(min_value=1, max_value=100000),
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_ratio_add(ratio_factory, x, y, z, k):
    ratio = ratio_factory

    base = (to_uint(x), to_uint(y))  # x/y
    other = (to_uint(z), to_uint(k))  # exponent

    root = await ratio.ratio_add(base, other).call()
    assert (from_uint(root.result[0][0]), from_uint(root.result[0][1])) == (
        (x * k + y * z, y * k) if y != k else (x + z, y)
    )
"""


@given(
    x=st.integers(min_value=4, max_value=10000),
    y=st.integers(min_value=3, max_value=10000),
    m=st.integers(min_value=2, max_value=7),
    p=st.integers(min_value=5, max_value=11),
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_nth_root_by_digit(ratio_factory, x, y, m, p):
    ratio = ratio_factory

    base = (to_uint(2), to_uint(1))  # x/y
    root = to_uint(2)  # which root
    precision = 5  # how many digits

    root = await ratio.nth_root_by_digit(base, root, precision).call()
    res = math.floor(((x / y) ** (1 / m)) * 10 ** p) / (10 ** p)
    assert (from_uint(root.result[0][0]) / from_uint(root.result[0][1]) - res) < (
        5 / (10 ** p)
    )
