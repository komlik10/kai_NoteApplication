from django.urls import path
from .views import NoteListView, NoteDetailView, NoteCreateView, NoteDeleteView



urlpatterns = [
    path('', NoteListView.as_view(), name='home'),
    path('create/', NoteCreateView.as_view(), name='note_create'),
    path('<str:slug>/', NoteDetailView.as_view(), name='note_detail'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete')
]
