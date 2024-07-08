from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin
from .models import Category, Note

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель модели категорий
    """
    list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)} 
