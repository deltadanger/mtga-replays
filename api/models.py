import logging

from django.db import models
from django_extensions.db.fields.json import JSONField

logger = logging.getLogger(__name__)


class Game(models.Model):
    player = JSONField(default={})
    opponent = JSONField(default={})
    player_deck = JSONField(default={})

    player_played_cards = JSONField(default=[])
    opponent_played_cards = JSONField(default=[])

    game_states = JSONField(default=[])
    instance_mapping = JSONField(default={})

    def __str__(self):
        return f"{self.player['playerName']} VS {self.opponent['playerName']}"
