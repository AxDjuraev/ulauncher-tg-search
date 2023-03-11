from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from filters import filter_
from utils import (download_profile_photo, icon_file, limit, s, search_chat,
                   sync_client)


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
