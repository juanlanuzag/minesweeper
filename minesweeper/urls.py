from django.urls import include, path
from rest_framework import routers
from game.views import MinesweeperGameViewSet

router = routers.DefaultRouter()
router.register(r'minesweeper', MinesweeperGameViewSet, basename='minesweeper')

urlpatterns = [
    path('api/', include(router.urls)),
]
