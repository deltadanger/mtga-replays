from rest_framework.fields import JSONField
from rest_framework.serializers import ModelSerializer

from api.models import Game


class GameSerializer(ModelSerializer):
    player = JSONField()
    opponent = JSONField()
    player_deck = JSONField()
    player_played_cards = JSONField()
    opponent_played_cards = JSONField()
    game_states = JSONField()
    instance_mapping = JSONField()

    class Meta:
        model = Game
        fields = '__all__'

