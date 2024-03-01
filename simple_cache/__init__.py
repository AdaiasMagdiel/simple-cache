from .providers.provider import Provider

__version__ = "1.0.0"


class SimpleCache:
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def init_provider(self, **kwargs):
        self.provider.init(**kwargs)
