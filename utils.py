from asyncio import new_event_loop
from os.path import dirname

from telethon import TelegramClient
from telethon.tl.functions.contacts import SearchRequest

from filters import filter_

loop = new_event_loop()
icon_file = 'images/icon.png'
client: TelegramClient = None
limit = 10
images_path = f'{dirname(__file__)}/images'


async def download_profile_photo(chat_entity):
    if chat_entity.photo:
        fname = f'{images_path}/{chat_entity.id}.jpg'
        with open(fname, "wb") as photo_file:
            photo = await client.download_profile_photo(
                chat_entity,
                file=photo_file,
                download_big=False
            )
        if photo:
            return fname
    return 'images/icon.png'


def s(f):
    return loop.run_until_complete(f)


async def search_chat(query='', limit=10):
    if not query or query.strip() == "":
        return []
    results = await client(
        SearchRequest(
            query,
            limit=limit,
        ),
    )
    if not results:
        return []
    results = sorted(results.users + results.chats, key=filter_)
    results[:limit]
    return results


async def sync_client(extension):
    global client
    if client is None:
        api_id = extension.preferences['telegram_client_api_id']
        api_hash = extension.preferences['telegram_client_api_hash']
        session_path = extension.preferences['telegram_client_session_path']
        print(session_path)
        client = TelegramClient(
            session_path,
            api_id=int(api_id),
            api_hash=api_hash
        )
        await client.connect()
        is_authorized = await client.is_user_authorized()
        print(is_authorized)
        print(__file__)
        if not is_authorized:
            raise ValueError("Client is not authorized!")
    else:
        await client.connect()
