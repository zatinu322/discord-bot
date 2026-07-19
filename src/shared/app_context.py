from contextvars import ContextVar

from .config import Config

config = Config()

config_var: ContextVar[Config] = ContextVar("config_var", default=config)


def get_config() -> Config:
    return config_var.get()
