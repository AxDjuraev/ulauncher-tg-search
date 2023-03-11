import logging
from asyncio import new_event_loop
from os.path import dirname

from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import SearchRequest
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

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


class TelegramSeachExtension(Extension):
    def __init__(self):
        super(TelegramSeachExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        try:
            s(sync_client(extension))
            query = event.get_argument() or str()

            if len(query.strip()) == 0:
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon=icon_file,
                        name='No input',
                        on_enter=HideWindowAction()
                    )
                ])

            res = []
            dialoges = s(search_chat(query, limit=limit))
            if not dialoges:
                res.append(
                    ExtensionResultItem(
                        icon=icon_file,
                        name='Not Found',
                        on_enter=HideWindowAction()
                    )
                )
            for dialog in dialoges:
                title = filter_(dialog)
                photo_path = s(download_profile_photo(dialog))
                res.append(
                    ExtensionResultItem(
                        icon=photo_path,
                        name=title,
                        on_enter=OpenUrlAction(f'tg://chat?id={dialog.id}')
                    )
                )

            return RenderResultListAction(res)
        except ValueError:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon=icon_file,
                    name='Client NOT Authorized',
                    on_enter=HideWindowAction()
                )
            ])


if __name__ == "__main__":
    TelegramSeachExtension().run()
