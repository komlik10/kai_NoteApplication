from django.views.generic import ListView, DetailView, CreateView, DeleteView
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from .models import Note
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect
from .forms import NoteCreationForm, NoteUpdateForm
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

    def dispatch(self, request, *args):
        if request.user.is_authenticated == False:
            # Пользователь уже авторизован, перенаправляем на главную страницу
            return redirect('/login')
        return super().dispatch(request, *args,)

    def get_queryset(self):
        user = self.request.user
        # if user == None:
        #     return redirect('login/')
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

class NoteUpdateView(UpdateView):
    """
    Представление: обновление заметки на сайте
    """
    model = Note
    template_name = 'note/note_update.html'  # Шаблон для отображения формы обновления
    form_class = NoteUpdateForm  # Класс формы для валидации данных формы
    pk_url_kwarg = 'pk'  # Имя аргумента URL, содержащего первичный ключ объекта

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user  # Устанавливаем автора как текущего пользователя
        return super().form_valid(form)


class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('home')  # Используйте reverse_lazy для определения URL-адреса перенаправления
    template_name = 'note/note_delete_confirm.html'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        # Здесь можно добавить дополнительную логику, например, проверку прав доступа
        obj.delete()
        return redirect('home')  # Используйте redirect для перенаправления на главную страницу
