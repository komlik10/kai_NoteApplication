from django.urls import path
from .views import NoteListView, NoteDetailView, NoteCreateView



urlpatterns = [
    path('', NoteListView.as_view(), name='home'),
    path('create/', NoteCreateView.as_view(), name='note_create'),
    path('<str:slug>/', NoteDetailView.as_view(), name='note_detail'),
]
