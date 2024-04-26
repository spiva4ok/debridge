from debridge.core.config import Config
from debridge.core import loading
from debridge.bridge.general import BridgeHandler


def perform(config: Config, wallets: list[str], proxies: list[str]) -> None:
    handler = BridgeHandler(config, wallets, proxies)
    handler.handle()


def main():
    config = Config(loading.load_config_payload())
    wallets = loading.load_wallets()
    proxies = loading.load_proxies()
    perform(config, wallets, proxies)


if __name__ == "__main__":
    main()
