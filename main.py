from amino import Client
from amino.Decorators import Start

from asyncio import gather, create_task

print("""\033[0;34m
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢘⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀AminoSpamBot
⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀
⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⣿⣆⠀
⠏⢿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠘⣿⠀
⠀⢨⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣿⠁
⠀⠀⠛⠉⠙⢿⣿⣿⣿⣿⣿⣿⣿⠁⠙⠋⠈⠁⠀
⠀⠀⠀⠀⠀⣿⣿⠇⠈⠉⠛⢿⣿⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠈⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⢸⣿⡆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣇⠀⠀⠀⠀⠀⢸⣿⣧⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠛⠛⠀⠀⠀⠀⠀⠀⠛⠛⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""")


async def login(client: Client) -> None:
    try:
        await client.auth(input("\033[0;34mEmail::: "), input("\033[0;34mPassword::: "))
    except Exception as ex:
        print("\033[1;31m{0}".format(ex))
        await login(client)


async def choice_community(client: Client) -> int:
    communities = await client.get_communities()
    for _, name in enumerate(communities.name, 1):
        print("{0}.{1}".format(_, name))
    return communities.ndcId[int(input("Select >>> ")) - 1]


async def choice_chat(client: Client, ndcId: int) -> str:
    chats = await client.get_chats(ndcId)
    for _, title in enumerate(chats.title, 1):
        print("{0}.{1}".format(_, title))
    return chats.threadId[int(input("Select >>> ")) - 1]


async def send_message(client: Client, ndcId: int, threadId: str, text: str, message_type: int) -> None:
    while True:
        await gather(*[create_task(client.send_message(ndcId=ndcId,
                                                       text=text,
                                                       threadId=threadId,
                                                       message_type=message_type)) for _ in range(450)])


@Start()
async def main(client: Client):
    await login(client)
    ndcId = await choice_community(client)
    await send_message(client=client,
                       ndcId=ndcId,
                       threadId=await choice_chat(client, ndcId),
                       text=input("Message::: "),
                       message_type=int(input("Message Type::: ")))
    print("Spamming...")
