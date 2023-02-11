from .Client import Client
from asyncio import get_event_loop


class Start:
    def __init__(self) -> None:
        self.client = Client()

    def __call__(self, function, *args, **kwargs) -> None:
        get_event_loop().run_until_complete(function(self.client, *args, **kwargs))