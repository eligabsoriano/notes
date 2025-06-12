# notes/serializers.py
from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    """Serializer for the Note model to handle JSON conversion for API endpoints."""
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'image', 'author']
        read_only_fields = ['author', 'created_at', 'updated_at']  # Prevent modification via API