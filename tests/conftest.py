import os
import asyncio
import pytest

from starkware.starknet.testing.starknet import Starknet

# contract and library paths
RATIO_CONTRACT = os.path.join(os.path.dirname(__file__), "../contracts/ratio.cairo")


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.new_event_loop()


# contract and object factories
@pytest.fixture(scope="module")
async def starknet_factory():
    starknet = await Starknet.empty()
    return starknet


@pytest.fixture(scope="module")
async def ratio_factory(starknet_factory):
    starknet = starknet_factory

    # Deploy the account contract
    ratio_contract = await starknet.deploy(source=RATIO_CONTRACT)

    return ratio_contract
