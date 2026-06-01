from django.urls import path
from .views import (
    RegisterView, LoginView,
    AssignTrainerCenterView, TrainerListView, UnassignTrainerCenterView,
    TrainerDetailView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),

    path("assign-trainer-centers/", AssignTrainerCenterView.as_view()),
    path("unassign-trainer-centers/", UnassignTrainerCenterView.as_view()),

    path("trainers/", TrainerListView.as_view()),
    path("trainers/<int:id>/", TrainerDetailView.as_view()),
]