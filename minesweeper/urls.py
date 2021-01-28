from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from game.views import MinesweeperGameViewSet

router = routers.DefaultRouter()
router.register(r'minesweeper', MinesweeperGameViewSet, basename='minesweeper')

urlpatterns = [
    path('api/', include(router.urls)),
    path('openapi/', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
