from aiohttp import ClientSession
from ujson import loads, dumps

from time import time

from .Utils import Utils
from .Objects import *


class Client:
    def __init__(self) -> None:
        self.url: str = "https://service.narvii.com/api/v1"
        self.sid: str or None = None
        self.device_id: str = Utils.generate_deviceid()
        self.session: ClientSession = ClientSession()


    def get_headers(self, data = None) -> dict[str, str]:
        headers: dict[str, str] = {
            "ndcdeviceid": self.device_id,
            "accept-language": "en-us",
            "content-type": "application/json",
            "user-agent": "Bot: amino lib",
            "host": "service.narvii.com",
            "connection": "upgrade"
        }

        if self.sid:
            headers["ndcauth"] = "sid={0}".format(self.sid)

        if data:
            headers["ndc-msg-sig"] = Utils.generate_signature(data)

        return headers


    async def auth(self, email: str, password: str) -> Me:
        body = dumps({
            "email": email,
            "secret": "0 {0}".format(password),
            "deviceID": self.device_id,
            "action": "normal",
            "clientType": 100,
            "v": 2,
            "timestamp": int(time() * 1000)
        })

        async with self.session.post("{0}/g/s/auth/login".format(self.url),
                                     data=body,
                                     headers=self.get_headers(body)) as response:
            if response.status != 200:
                raise Exception(await response.text())

            data = loads(await response.text())

            self.sid = data["sid"]

            return Me.Me(data)


    async def exit(self) -> None:
        body = dumps({
            "deviceID": self.device_id,
            "clientType": 100,
            "timestamp": int(time() * 1000)
        })

        async with self.session.post("{0}/g/s/auth/logout".format(self.url),
                                     data=body,
                                     headers=self.get_headers(body)) as response:
            if response.status != 200:
                raise Exception(await response.text())


    async def get_communities(self) -> CommunityList:
        async with self.session.get("{0}/g/s/community/joined?v=1&start=0&size=100".format(self.url),
                                    headers=self.get_headers()) as response:
            if response.status != 200:
                raise Exception(await response.text())

            return CommunityList.CommunityList(loads(await response.text())["communityList"])


    async def get_chats(self, ndcId: int) -> ChatList:
        async with self.session.get("{0}/x{1}/s/chat/thread?type=joined-me&start=0&size=100".format(self.url, ndcId),
                                    headers=self.get_headers()) as response:
            if response.status != 200:
                raise Exception(await response.text())

            return ChatList.ChatList(loads(await response.text())["threadList"])


    async def send_message(self, ndcId: int, text: str, message_type: int, threadId: str) -> None:
        body = dumps({
            "type": message_type,
            "content": text,
            "clientRefId": int(time() / 10 % 1000000000),
            "attachedObject": {
                "objectId": None,
                "objectType": None,
                "link": None,
                "title": None,
                "content": None,
                "mediaList": None
            },
            "extensions": {"mentionedArray": []},
            "timestamp": int(time() * 1000)
        })

        async with self.session.post("{0}/x{1}/s/chat/thread/{2}/message".format(self.url, ndcId, threadId),
                                     data=body,
                                     headers=self.get_headers(body)) as response:
            if response.status != 200:
                raise Exception(await response.text())