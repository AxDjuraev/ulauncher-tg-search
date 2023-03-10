import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


icon_file='images/icon.png'


class TelegramSeachExtension(Extension):
    def __init__(self):
        super(TelegramSeachExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, )


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
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

