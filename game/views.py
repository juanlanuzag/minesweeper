from rest_framework import viewsets

from game.models import Game
from game.serializers import GameSerializer


class MinesweeperGameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
