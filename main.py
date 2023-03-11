import logging
from asyncio import new_event_loop

from telethon.sync import TelegramClient
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

loop = new_event_loop()
icon_file='images/icon.png'
client: TelegramClient = None
limit = 10


def s(f):
    return loop.run_until_complete(f)


async def get_dialoges(limit=10):
    async_dialoges = client.iter_dialogs()
    res = []
    c = 0
    async for dialog in async_dialoges:
        res.append(dialog)
        c += 1
        if c >= limit:
            break
    return res


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
            dialoges = s(get_dialoges(limit=limit))
            for dialog in dialoges:
                res.append(
                    ExtensionResultItem(
                        icon=icon_file,
                        name=dialog.title,
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

