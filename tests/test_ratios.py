import pytest
import math
from hypothesis import given, strategies as st, settings

"""
@given(
    x=st.integers(min_value=1, max_value=10000000000000000),
    y=st.integers(min_value=1, max_value=10000000000000000),
    z=st.integers(min_value=1, max_value=10000000000000000),
    k=st.integers(min_value=1, max_value=10000000000000000),
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_ratio_diff(ratio_factory, x, y, z, k):
    ratio = ratio_factory

    base = (x, y)  # 1/4
    other = (z, k)  # 1/3

    root = await ratio.ratio_diff(base, other).call()

    assert root.result[0] == (
        (
            abs(z * y - x * k),
            k * y,
        )
        if k != y
        else (abs(z - x), k)
    )


@given(
    x=st.integers(min_value=1, max_value=10000000000000000),
    y=st.integers(min_value=1, max_value=10000000000000000),
    z=st.integers(min_value=1, max_value=10000000000000000),
    k=st.integers(min_value=1, max_value=10000000000000000),
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_ratio_le_eq(ratio_factory, x, y, z, k):
    ratio = ratio_factory

    base = (x, y)  # x/y
    other = (z, k)  # z/k

    root = await ratio.ratio_less_than_or_eq(base, other).call()
    assert root.result[0] == (1 if x / y <= z / k else 0)


@given(
    x=st.integers(min_value=1, max_value=100),
    y=st.integers(min_value=1, max_value=100),
    z=st.integers(min_value=1, max_value=15),
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_ratio_pow(ratio_factory, x, y, z):
    ratio = ratio_factory

    base = (x, y)  # 3/1
    power = z  # exponent

    root = await ratio.ratio_pow(base, power).call()
    assert root.result[0] == (x ** z, y ** z)
"""


@pytest.mark.asyncio
async def test_nth_root(ratio_factory):
    ratio = ratio_factory

    base = (2134801878974, 74893271)  # 9/1
    root = 2  # cube root
    error = (10, 1)  # .01

    root = await ratio.ratio_nth_root(base, root, error).call()
    print(root)
    # assert root.result[0] == (3, 1)
