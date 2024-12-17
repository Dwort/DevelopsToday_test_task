from django.urls import path
from .views import (
    CreateCatAgent,
    GetAllCats,
    SingleCatEdits,
)

urlpatterns = [
    path('add_cat/', CreateCatAgent.as_view()),
    path('all_cats/', GetAllCats.as_view()),
    path('cat/<int:cat_id>/', SingleCatEdits.as_view()),
]
