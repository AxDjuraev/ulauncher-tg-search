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


def s(f):
    return loop.run_until_complete(f)

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

        res = [
            ExtensionResultItem(
                icon=icon_file,
                name='axdjuraev2',
                on_enter=OpenUrlAction(f'https://t.me/c/axdjuraev')
            ),
            ExtensionResultItem(
                icon=icon_file,
                name='JuraevNozimjon',
                on_enter=OpenUrlAction(f'https://t.me/c/JuraevNozimjon')
            )
        ]

        return RenderResultListAction(res)


if __name__ == "__main__":
    TelegramSeachExtension().run()

