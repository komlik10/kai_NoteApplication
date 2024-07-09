from django.views.generic import ListView, DetailView, CreateView, DeleteView
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from .models import Note
from .forms import NoteCreationForm
from rest_framework.generics import ListAPIView
from .serializers import NoteSerializer
from django.http import HttpResponseRedirect

class UserNotesView(ListAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        author = self.request.user
        return Note.objects.filter(user=author)


# class NoteListView(ListView):
#     model = Note
#     template_name = 'note/note_list.html'
#     context_object_name = 'articles'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Главная страница'
#         return context

# class NoteListView(ListAPIView):
#     serializer_class = NoteSerializer
#     model = Note
#     template_name = 'note/note_list.html'
#     context_object_name = 'articles'

#     def get_queryset(self):
#         user = self.request.user
#         if not user.is_authenticated:
#             raise PermissionDenied("Access denied")
#         return Note.objects.filter(author=user)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Главная страница'
#         return context
from django.views.generic import ListView

class NoteListView(ListView):
    model = Note
    template_name = 'note/note_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def get_context_data(self, *kwargs):
        context = super().get_context_data(*kwargs)
        context['title'] = 'Главная страница'
        context['author_name'] = str(self.request.user.username)
        return context

class NoteDetailView(DetailView):
    model = Note
    template_name = 'note/note_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class NoteCreateView(CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Note
    template_name = 'note/note_create.html'
    form_class = NoteCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class NoteDeleteView(DeleteView):
    """
    Представление: удаление заметки без подтверждения
    """
    model = Note
    template_name = ''  # Установите пустое значение, чтобы не использовать шаблон подтверждения

    def delete(self, request, *args, **kwargs):
        """
        Метод delete переопределяется для добавления дополнительной логики перед удалением,
        например, проверка прав доступа.
        """
        obj = self.get_object()
        if not request.user == obj.author:
            raise PermissionDenied("У вас нет разрешения на удаление этой заметки.")
        
        # Удаление заметки
        obj.delete()
        
        # Перенаправление на главную страницу
        return HttpResponseRedirect(reverse_lazy('home'))  # Замените 'home' на имя URL-маршрута вашей главной страницы
