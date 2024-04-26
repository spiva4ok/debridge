import random
import time

from loguru import logger
from web3 import Web3
from web3.exceptions import Web3Exception

from debridge.core.constants import NETWORK_RPC_URLS


def build_web3(network: str, proxy: str | None = None) -> Web3:
    url = NETWORK_RPC_URLS[network]
    if not proxy:
        return Web3(Web3.HTTPProvider(url))

    return Web3(
        Web3.HTTPProvider(
            url, request_kwargs={"proxies": {"https": proxy, "http": proxy}}
        )
    )


def estimate_gas(web3: Web3, tx: dict) -> int:
    try:
        return web3.eth.estimate_gas(tx)
    except Web3Exception as error:
        gas = random.randint(2000000, 3000000)
        logger.warning(
            f"Could not estimate gas, so use random value {gas}. Error: {error}"
        )
        return gas


def wait_for_gas(web3: Web3, tx: dict, max_gas: int) -> int:
    while True:
        gas = estimate_gas(web3, tx)
        if gas <= max_gas:
            return gas
        time_to_sleep = random.randint(5, 10)
        logger.warning(
            f"Gas is too high: {gas}. " f"Sleep {time_to_sleep} sec and try again."
        )
        time.sleep(time_to_sleep)


def sign_and_send_tx(web3: Web3, tx: dict, private_key: str) -> bool:
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    raw_tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = web3.to_hex(raw_tx_hash)

    receipt = get_transaction_receipt(tx_hash, web3)
    success = receipt["status"] == 1

    return success


def get_transaction_receipt(tx_hash: bytes, w3: Web3) -> dict:
    times = [1, 2, 3, 3, 6, 7, 10]
    receipt = None
    for secs in times:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
        except Web3Exception:
            time.sleep(secs)
            continue
        status = receipt.get("status")

        if status in {0, 1}:
            return receipt

        time.sleep(secs)

    return receipt
