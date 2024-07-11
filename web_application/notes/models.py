from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from modules.services.utils import unique_slugify


class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_note_categories'

    def __str__(self):
        """
        Возвращение заголовка статьи
        """
        return self.title


User = get_user_model()


class Note(models.Model):
    """
    Модель постов для сайта
    """    
    STATUS_OPTIONS = (
        ('published', 'Основное'), 
        ('archive', 'Архив')
    )
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    full_description = models.TextField(verbose_name='Полное описание')
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус заметки', max_length=10)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts', default=1)


    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'pk': self.pk})  


    def save(self, *args, **kwargs):
            """
            Сохранение полей модели при их отсутствии заполнения
            """
            if not self.slug:
                self.slug = unique_slugify(self, self.title)
            super().save(*args, **kwargs)


    class Meta:
        db_table = 'app_notes'
        ordering = ['-time_create']
        indexes = [models.Index(fields=['status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title
