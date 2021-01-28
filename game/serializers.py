from rest_framework import serializers

from game.minesweeper import MinesweeperGame
from game.models import Game


class GameSerializer(serializers.ModelSerializer):
    board = serializers.SerializerMethodField()
    is_over = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'rows', 'columns', 'mines', 'was_lost', 'was_won', 'board', 'is_over']
        extra_kwargs = {
            'was_lost': {'read_only': True},
            'was_won': {'read_only': True}
        }

    def get_board(self, obj):
        return MinesweeperGame.get_visible_board_state(obj.board)

    def get_is_over(self, obj):
        return obj.was_won or obj.was_lost

    def create(self, validated_data):
        columns = validated_data.get('columns')
        rows = validated_data.get('rows')
        mines = validated_data.get('mines')
        game = MinesweeperGame.new_game(columns=columns, rows=rows, mines=mines)
        return Game.objects.create_from_minesweeper_game(game)
