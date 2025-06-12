# notes/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notes', views.NoteViewSet, basename='note')  # Added basename to fix AssertionError

urlpatterns = [
    path('', include(router.urls)),  # Include all ViewSet routes
]