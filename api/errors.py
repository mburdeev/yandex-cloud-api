from typing import Optional


class YandexAPIError(Exception):
    def __init__(self, code: int, message: str, details: Optional[dict]) -> None:
        super().__init__(code, message, details)
        self.code = code
        self.message = message
        self.details = details

    def __str__(self) -> str:
        return f"Code {self.code}: {self.message}"
