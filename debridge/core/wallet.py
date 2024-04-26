from eth_account.signers.local import LocalAccount
from web3 import Web3


class Wallet:
    def __init__(self, web3: Web3, private_key: str) -> None:
        self.web3 = web3
        self.private_key = private_key

        self._account = None

    @property
    def account(self) -> LocalAccount:
        if self._account is None:
            self._account = self.web3.eth.account.from_key(self.private_key)
        return self._account

    @property
    def address(self) -> str:
        return self.account.address

    @property
    def nonce(self) -> int:
        return self.web3.eth.get_transaction_count(self.address)

    @property
    def eth_balance(self) -> int:
        return self.web3.eth.get_balance(self.address)
