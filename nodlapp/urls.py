from django.urls import path
from .views import *
from . import views
import uuid


urlpatterns = [
    path('', MultipleModelView.as_view(), name='nodl-home'),
    path('subject/<uuid:pk>/', SubjectDetailView.as_view(), name='subject-detail'),
    path('week/<uuid:pk>/', WeekDetailView.as_view(), name='week-detail'),
    path('week/<uuid:pk>/submission/', CreateSubmissionView.as_view(), name='create-submission'),
]