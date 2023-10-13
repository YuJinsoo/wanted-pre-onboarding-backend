from django.contrib import admin
from django.urls import path, include

from .views import JobOpeningListView, JobOpeningCreateView,JobOpeningView


app_name = "recruit"

urlpatterns = [
    path("jobopening/list/", JobOpeningListView.as_view()),
    path("jobopening/", JobOpeningCreateView.as_view()),
    path("jobopening/<int:jo_pk>/", JobOpeningView.as_view()),
]
