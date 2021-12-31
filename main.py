import requests
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)


class NpmjsExtension(Extension):

    def __init__(self):
        super(NpmjsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        searchKeyword = event.get_argument()
        searchSize = extension.preferences['npmjs_max_search_result_size']
        if not searchKeyword:
            return

        url = 'https://registry.npmjs.com/-/v1/search?text={}&size=5'.format(
            searchKeyword, searchSize)
        # logger.debug(url)

        response = requests.get(url, headers={'User-Agent': 'ulauncher-npmjs'})
        data = response.json()
        # logger.debug(data)

        items = []
        for result in data['objects']:
            package = result['package']
            # logger.debug(package)
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=package['name'],
                                             description=package['description'],
                                             on_enter=OpenUrlAction(package['links']['npm'])))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data['package']['name'],
                                                           description=data['package']['description'],
                                                           on_enter=OpenUrlAction(data['package']['links']['npm']))])


if __name__ == '__main__':
    NpmjsExtension().run()
