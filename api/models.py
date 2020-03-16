from django.db import models
from django_extensions.db.fields.json import JSONField


class Game(models.Model):
    current_player = JSONField(default={})
    opponent = JSONField(default={})
    current_player_deck = JSONField(default={})

    current_player_played_cards = JSONField(default=[])
    opponent_played_cards = JSONField(default=[])

    board_states = JSONField(default=[])
    instance_mapping = JSONField(default={})

    def __str__(self):
        return f"{self.current_player} VS {self.opponent}"
