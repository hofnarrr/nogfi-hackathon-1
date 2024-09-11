from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    username: str
    password: str
    host: str
    port: int
    interface_numbers: list[int] = list(range(49)) + list(range(52, 77, 4))
