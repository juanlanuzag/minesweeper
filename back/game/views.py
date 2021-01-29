from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from game.minesweeper import MinesweeperException
from game.models import Game
from game.serializers import GameSerializer


class MinesweeperGameViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True, methods=['post'])
    def flag_cell(self, request, *args, **kwargs):
        x_position = request.data.get('x_position')
        y_position = request.data.get('y_position')
        is_flagged = request.data.get('is_flagged')
        if x_position is None or y_position is None or is_flagged is None:
            raise ValidationError('x_position, y_position and is_flagged are required fields')

        instance = self.get_object()
        minesweeper_game = instance.to_minesweeper_game()
        try:
            minesweeper_game.set_flag_on_cell_position(x_position, y_position, is_flagged)
        except MinesweeperException as e:
            raise ValidationError(e)

        instance.update_from_minesweeper_game(minesweeper_game)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reveal_cell(self, request, *args, **kwargs):
        x_position = request.data.get('x_position')
        y_position = request.data.get('y_position')
        if x_position is None or y_position is None:
            raise ValidationError('x_position and y_position are required fields')

        instance = self.get_object()
        minesweeper_game = instance.to_minesweeper_game()
        try:
            minesweeper_game.reveal_cell_position(x_position, y_position)
        except MinesweeperException as e:
            raise ValidationError(e)

        instance.update_from_minesweeper_game(minesweeper_game)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
