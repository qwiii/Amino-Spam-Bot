class Me:
    @classmethod
    def Me(cls, json: str):
        try:
            cls.auid = json["auid"]
            cls.nickname = json["account"]["nickname"]
            cls.icon = json["account"]["icon"]
            cls.aminoId = json["account"]["aminoId"]
            cls.secret = json["account"]["secret"]
            cls.securityLevel = json["account"]["securityLevel"]
            cls.role = json["account"]["role"]
            cls.adsEnabled = json["account"]["adsEnabled"]
        except (KeyError, TypeError):
            pass

        return cls

class CommunityList:
    @classmethod
    def CommunityList(cls, json: str):
        cls.name = []
        cls.icon = []
        cls.link = []
        cls.ndcId = []
        cls.content = []
        cls.activeInfo = []

        for _ in json:
            try:
                cls.name.append(_["name"])
                cls.icon.append(_["icon"])
                cls.link.append(_["link"])
                cls.ndcId.append(_["ndcId"])
                cls.content.append(_["content"])
                cls.activeInfo.append(_["activeInfo"])
            except (KeyError, TypeError):
                pass

        return cls

class ChatList:
    @classmethod
    def ChatList(cls, json: str):
        cls.title = []
        cls.status = []
        cls.threadId = []

        for _ in json:
            try:
                cls.title.append(_["title"])
                cls.status.append(_["status"])
                cls.threadId.append(_["threadId"])
            except (KeyError, TypeError):
                pass

        return cls