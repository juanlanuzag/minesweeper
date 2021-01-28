from django.db import models


class Game(models.Model):
    rows = models.PositiveIntegerField()
    columns = models.PositiveIntegerField()
    mines = models.PositiveIntegerField()
    was_lost = models.BooleanField(default=False)
    was_won = models.BooleanField(default=False)
    board = models.JSONField()
