import random
import time

from loguru import logger

from debridge.bridge.wallet import WalletHandler
from debridge.core.config import Config


class BridgeHandler:
    def __init__(self, config: Config, wallets: list[str], proxies: list[str]) -> None:
        self.config = config
        self.wallets = wallets
        self.proxies = proxies

    def handle(self) -> None:
        wallets = self.wallets
        proxies = self.proxies
        logger.info(f"Number of wallets: {len(wallets)}")
        logger.info(f"Number of proxies: {len(proxies)}")

        if proxies and len(wallets) != len(proxies):
            logger.error("Number of wallets should equal number of proxies")
            return None

        indexes = list(range(len(wallets)))
        if self.config.randomise_order:
            random.shuffle(indexes)

        for order_index, index in enumerate(indexes):
            private_key = wallets[index]
            proxy = proxies[index] if proxies else None

            wallet_title = private_key[:6] + "..." + private_key[-6:]
            logger.info(
                f"Start wallet {wallet_title} ({order_index + 1} out of {len(wallets)})"
            )

            wallet_handler = WalletHandler(self.config, private_key, proxy)
            logger.info(f"Wallet address: {wallet_handler.wallet_address}")

            try:
                status = wallet_handler.handle()
            except Exception as error:
                status = False
                logger.error(f"Unexpected error happened: {error}")

            if status:
                logger.info(f"Order was successfully submitted")
            else:
                logger.error(f"Order was submitted but failed to be processed")

            logger.info(
                f"Finish wallet {wallet_title} ({order_index + 1} out of {len(wallets)}). \n"
            )

            if private_key != wallets[-1]:
                self.wait_before_next_wallet()

    def wait_before_next_wallet(self):
        timeout = random.uniform(self.config.timeout["min"], self.config.timeout["max"])
        logger.info(f"Sleeping for {timeout} seconds\n")
        time.sleep(timeout)
