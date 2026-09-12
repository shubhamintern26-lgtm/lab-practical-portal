from django.urls import path

from . import views


urlpatterns = [
    path(
        "ask/",
        views.ask_ai_view,
        name="ask_ai"
    ),
]