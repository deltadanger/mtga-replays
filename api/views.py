
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Game
from api.serializers import GameSerializer


class GamesViewSet(ReadOnlyModelViewSet):
    queryset = Game.objects.all()[:3]
    serializer_class = GameSerializer
