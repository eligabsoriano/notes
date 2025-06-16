from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Note
from .forms import NoteForm
from .serializers import NoteSerializer
from django.contrib.auth.models import User

# Custom permission class to check if user is a superuser
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

@login_required
def note_list(request):
    # If user is superuser, show all notes from all users
    # Otherwise, show only the user's own notes
    if request.user.is_superuser:
        # Get filter parameter from request
        filter_type = request.GET.get('filter', 'all')
        
        if filter_type == 'superusers':
            # Get all superusers
            superusers = User.objects.filter(is_superuser=True)
            notes = Note.objects.filter(author__in=superusers)
        elif filter_type == 'regular_users':
            # Get all regular users
            regular_users = User.objects.filter(is_superuser=False)
            notes = Note.objects.filter(author__in=regular_users)
        else:
            # Show all notes
            notes = Note.objects.all()
    else:
        notes = Note.objects.filter(author=request.user)
    
    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'filter_type': request.GET.get('filter', 'all')
    })

@login_required
def note_create(request):
    # Allow any authenticated user to create notes
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_update(request, pk):
    # Get the note regardless of author (needed for superuser view)
    note = get_object_or_404(Note, pk=pk)
    
    # RBAC: Only the original author can update their notes
    # Superusers cannot modify notes, they can only view and delete
    if not request.user.is_superuser and note.author != request.user:
        return redirect('note_list')
    
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_delete(request, pk):
    # Get the note regardless of author (needed for superuser view)
    note = get_object_or_404(Note, pk=pk)
    
    # RBAC: Both superusers and note authors can delete notes
    if not request.user.is_superuser and note.author != request.user:
        return redirect('note_list')
        
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Superusers can see all notes, regular users only see their own
        if self.request.user.is_superuser:
            return Note.objects.all()
        return Note.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the current user as the author
        serializer.save(author=self.request.user)

    def get_permissions(self):
        # Special permission handling for delete action
        # Only superusers can delete notes through the API
        if self.action in ['destroy']:
            return [IsAuthenticated(), IsSuperUser()]
        return [IsAuthenticated()]