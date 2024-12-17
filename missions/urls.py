from django.urls import path
from .views import (
    CreateMissionAndTargets,
    GetAllMission,
    MissionEdits,
    AssignCatToMission,
    UpdateTargetMark,
    UpdateTargetNotes,
)


urlpatterns = [
    path('mission/create/', CreateMissionAndTargets.as_view()),
    path('mission/all/', GetAllMission.as_view()),
    path('mission/<int:mission_id>/', MissionEdits.as_view()),
    path('mission/assign/', AssignCatToMission.as_view()),
    path('mission/target/mark/<int:target_id>/', UpdateTargetMark.as_view()),
    path('mission/target/notes/<int:target_id>/', UpdateTargetNotes.as_view()),
]