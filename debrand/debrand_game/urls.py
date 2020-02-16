from django.urls import path
from django.views.generic import TemplateView

from .views import character_customization_view, leaderboard_view, level_view

urlpatterns = [
    path('customize/', character_customization_view, name="character_customization"),
    path('leaderboard/', leaderboard_view, name="leaderboard"),
    path('level/<slug:level_slug>/', level_view, name="level"),
]