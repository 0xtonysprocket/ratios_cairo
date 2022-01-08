import pytest
import math
from hypothesis import given, strategies as st, settings
from starkware.starkware_utils.error_handling import StarkException, StarkErrorCode


@given(
    a=st.integers(min_value=2, max_value=256),
    b=st.integers(min_value=3, max_value=256),
    s_a=st.integers(
        min_value=-1, max_value=1).filter(lambda x: x != 0 & x != -1),
    s_b=st.integers(
        min_value=-1, max_value=1).filter(lambda x: x != 0 & x != 1)
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_safe_mul(ratio_factory, a, b, s_a, s_b):
    ratio = ratio_factory

    a_exp = int(math.pow(2, a)) * s_a
    b_exp = int(math.pow(2, b)) * s_b

    print(a_exp)
    print(b_exp)
    if a + b >= 128:
        with pytest.raises(StarkException) as execInfo:
            await ratio.safe_mul(a_exp, b_exp).call()
        print("overflow for ")
        print("a:${a} b:${b}")
        print("\n")
        assert execInfo.type is StarkException
    else:
        product = await ratio.safe_mul(a_exp, b_exp).call()
        print("product is ")
        print(product.result[0])
        print("-----")
        print(a_exp * b_exp)
        print("\n")
        assert product.result[0] == a_exp * b_exp


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


@given(
    x=st.integers(min_value=1, max_value=100000000000000),
    y=st.integers(min_value=1, max_value=100000000000000),
    m=st.integers(min_value=1, max_value=15),
    p=st.integers(min_value=5, max_value=11),
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_nth_root_by_digit(ratio_factory, x, y, m, p):
    ratio = ratio_factory

    base = (x, y)  # base fraction
    root = m  # which root
    precision = p  # how many digits

    root = await ratio.nth_root_by_digit(base, root, precision).call()
    res = math.floor(((x / y) ** (1 / m)) * 10 ** p) / (10 ** p)
    assert (root.result[0][0] / root.result[0][1] - res) < (5 / (10 ** p))
