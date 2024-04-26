import random

from debridge.core.constants import NETWORK_CHAIN_IDS
from debridge.core.config import Config
from debridge.core.wallet import Wallet
from debridge.core import web3 as w3
from debridge.bridge.services import DnlApiService


class WalletHandler:
    def __init__(self, config: Config, private_key: str, proxy: str | None = None):
        self.config = config
        self.private_key = private_key
        self.proxy = proxy

        self.api_service = DnlApiService(self.proxy)
        self.web3 = w3.build_web3(self.config.network["source"], proxy)
        self.wallet = Wallet(self.web3, private_key)
        self.wallet_address = self.wallet.address

    def handle(self) -> bool:
        amount = self.get_amount(self.wallet)
        order = self.create_order(amount)
        status = self.submit_order(order)
        return status

    def get_amount(self, wallet: Wallet) -> int:
        if self.config.amount.get("all"):
            # 100% - 0.002 ETH of the balance to cover gas fees
            return int(wallet.eth_balance - 0.0013 * 10**18)

        min_value = self.config.amount["min"]
        max_value = self.config.amount["max"]
        value = random.uniform(min_value, max_value)

        return int(value * 10**18)

    def create_order(self, amount: int) -> dict:
        query_params = {
            "srcChainId": NETWORK_CHAIN_IDS[self.config.network["source"]],
            "srcChainTokenIn": "0x0000000000000000000000000000000000000000",
            "srcChainTokenInAmount": str(amount),
            "dstChainId": NETWORK_CHAIN_IDS[self.config.network["destination"]],
            "dstChainTokenOut": "0x0000000000000000000000000000000000000000",
            "dstChainTokenOutAmount": "auto",
            "srcChainOrderAuthorityAddress": self.wallet_address,
            "dstChainTokenOutRecipient": self.wallet_address,
            "dstChainOrderAuthorityAddress": self.wallet_address,
        }

        data = self.api_service.create_order(query_params)

        return data

    def submit_order(self, order: dict) -> bool:
        tx = {
            **order["tx"],
            "nonce": self.wallet.nonce,
            "chainId": NETWORK_CHAIN_IDS[self.config.network["source"]],
            "value": int(order["tx"]["value"]),
        }

        gas = w3.wait_for_gas(self.web3, tx, self.config.max_gas)
        eth_gas_price = self.web3.eth.gas_price
        tx.update({"gas": gas})
        tx.update({"maxFeePerGas": eth_gas_price})
        tx.update({"maxPriorityFeePerGas": eth_gas_price})

        status = w3.sign_and_send_tx(self.web3, tx, self.private_key)

        return status
