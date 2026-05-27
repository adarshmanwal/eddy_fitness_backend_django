from django.urls import path

from .views import (
    CenterListCreateView,
    CenterDetailView
)

urlpatterns = [
    path(
        "",
        CenterListCreateView.as_view()
    ),

    path(
        "<int:pk>/",
        CenterDetailView.as_view()
    ),
]