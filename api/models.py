import logging

import requests
from django.db import models
from django_extensions.db.fields.json import JSONField


logger = logging.getLogger(__name__)


class Game(models.Model):
    current_player = JSONField(default={})
    opponent = JSONField(default={})
    current_player_deck = JSONField(default={})

    current_player_played_cards = JSONField(default=[])
    opponent_played_cards = JSONField(default=[])

    board_states = JSONField(default=[])
    instance_mapping = JSONField(default={})

    image_mapping = JSONField(default={})

    def __str__(self):
        return f"{self.current_player} VS {self.opponent}"

    def save(self, *args, **kwargs):

        logger.info("Fetching images...")
        for card in self.instance_mapping.values():
            if card['id'] in self.image_mapping:
                continue
            response = requests.get(f"https://api.scryfall.com/cards/arena/{card['id']}")
            if response.status_code == 404:
                response = requests.get(f"https://api.scryfall.com/cards/named?exact={card['name']}")

            card_image_details = response.json()['image_uris']
            self.image_mapping[card['id']] = {
                'normal': card_image_details.get('normal', card_image_details.get('small')),
                'large': card_image_details.get('large', card_image_details.get('normal', card_image_details.get('small'))),
            }
        logger.info("Done.")

        super().save(*args, **kwargs)
