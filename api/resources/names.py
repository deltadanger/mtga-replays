import json
import os


class _NamesGetter:

    mapping = {}

    def __getitem__(self, item):
        try:
            return self.mapping[item]
        except KeyError:
            file_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), 'data_loc.mtga'))
            with open(file_path, 'r', encoding='utf-8') as f:
                mapping_list = json.load(f)

            for mapping in mapping_list:
                if mapping.get('isoCode') != 'en-US':
                    continue

                for key in mapping.get('keys', []):
                    self.mapping[key['id']] = key['text']

        return self.mapping[item]


NAME_FROM_NAME_ID = _NamesGetter()


class _CardsGetter:

    mapping = {}

    def __getitem__(self, item):
        try:
            return NAME_FROM_NAME_ID[self.mapping[item]]
        except KeyError:
            file_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), 'data_cards.mtga'))
            with open(file_path, 'r', encoding='utf-8') as f:
                cards_list = json.load(f)

            self.mapping = {
                card['grpid']: card['titleId']
                for card in cards_list
            }

        return NAME_FROM_NAME_ID[self.mapping[item]]


NAME_FROM_CARD_ID = _CardsGetter()
