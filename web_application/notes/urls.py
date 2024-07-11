from django.urls import path
from .views import NoteListView, NoteDetailView, NoteCreateView, NoteDeleteView, NoteUpdateView


urlpatterns = [
    path('', NoteListView.as_view(), name='home'),
    path('create/', NoteCreateView.as_view(), name='note_create'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
    path('notes/<int:pk>/update/', NoteUpdateView.as_view(), name='note_update'),
]
