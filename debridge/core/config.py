from typing import Any


class Config:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    @property
    def module(self) -> str:
        return self.payload["module"]

    @property
    def current_module(self) -> dict:
        return self.payload["modules"][self.module]

    @property
    def network(self) -> dict[str, str]:
        return self.current_module["network"]

    @property
    def amount(self) -> dict[str, float | bool]:
        return self.current_module["amount"]

    @property
    def timeout(self) -> dict[str, int]:
        return self.current_module["timeout"]

    @property
    def max_gas(self) -> int:
        return self.current_module["max_gas"] * 100000  # Gwei * 100000

    @property
    def randomise_order(self) -> bool:
        return self.current_module["randomise_order"]
