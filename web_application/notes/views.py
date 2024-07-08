from django.views.generic import ListView, DetailView
from django.views.generic import CreateView

from .models import Note
from .forms import NoteCreationForm



class NoteListView(ListView):
    model = Note
    template_name = 'note/note_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
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
