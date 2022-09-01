from django.urls import path

from meal_plans.views import (
    MealPlansListView,
    MealPlansDeleteView,
    MealPlansDetailView,
    MealPlansCreateView,
    MealPlansEditView,
)

urlpatterns = [
    path("", MealPlansListView.as_view(), name="meal_plans_list"),
    path(
        "create/",
        MealPlansCreateView.as_view(),
        name="meal_plans_create",
    ),
    path(
        "<int:pk>/",
        MealPlansDetailView.as_view(),
        name="meal_plans_detail",
    ),
    path(
        "<int:pk>/edit",
        MealPlansEditView.as_view(),
        name="meal_plans_edit",
    ),
    path(
        "<int:pk>/delete",
        MealPlansDeleteView.as_view(),
        name="meal_plans_delete",
    ),
]
