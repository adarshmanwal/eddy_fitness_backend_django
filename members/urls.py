from django.urls import path

from .views import (
    MemberListCreateView,
    MemberDetailView,
    AssignMemberCenterView
)

urlpatterns = [

    path(
        "",
        MemberListCreateView.as_view()
    ),

    path(
        "<int:pk>/",
        MemberDetailView.as_view()
    ),
    path("assign-member-center/", AssignMemberCenterView.as_view()),
]