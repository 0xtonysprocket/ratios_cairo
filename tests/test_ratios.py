import pytest
import math
from hypothesis import given, strategies as st, settings
from starkware.starkware_utils.error_handling import StarkException, StarkErrorCode


# Cairo 5.2 does not handle negative numbers directly. Rather it needs to be subtracted from PRIME (2^251)
def minusPrime(num):
    prime = 3618502788666131213697322783095070105623107215331596699973092056135872020481
    return prime - num


@given(
    a=st.integers(min_value=2, max_value=256),
    b=st.integers(min_value=3, max_value=256),
    s_a=st.integers(
        min_value=-1, max_value=1).filter(lambda x: x != 0),
    s_b=st.integers(
        min_value=-1, max_value=1).filter(lambda x: x != 0)
)
@settings(deadline=None)
@pytest.mark.asyncio
async def test_safe_mul(ratio_factory, a, b, s_a, s_b):
    ratio = ratio_factory

    a_exp = int(math.pow(2, a))
    b_exp = int(math.pow(2, b))

    a_arg = a_exp
    b_arg = b_exp
    if s_a == -1:
        a_arg = minusPrime(a_exp)
    if s_b == -1:
        b_arg = minusPrime(b_exp)

    # If a + b > 128 then 2^a * 2^b > 2^241 which is the overflow threshold 
    if a + b >= 128:
        with pytest.raises(StarkException) as execInfo:
            await ratio.safe_mul(a_arg, b_arg).call()
        assert execInfo.type is StarkException
    else:
        product = await ratio.safe_mul(a_arg, b_arg).call()
        if s_a * s_b == 1:
            assert product.result[0] == a_exp * s_a * b_exp * s_b
        else:
            assert product.result[0] == minusPrime(a_exp * b_exp)


@given(
    x=st.integers(min_value=1, max_value=10000000000000000),
    y=st.integers(min_value=1, max_value=10000000000000000),
    z=st.integers(min_value=1, max_value=10000000000000000),
    k=st.integers(min_value=1, max_value=10000000000000000)
 )
@settings(deadline=None)
@pytest.mark.asyncio
async def test_ratio_mul(ratio_factory, x, y, z, k):
    ratio = ratio_factory
    
    base = (x, y) 
    other = (z, k)  

    product = await ratio.ratio_mul(base, other).call()
    assert product.result[0].n == x * z
    assert product.result[0].d == y * k



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
