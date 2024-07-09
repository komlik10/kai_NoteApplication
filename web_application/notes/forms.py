from django import forms

from .models import Note


class NoteCreationForm(forms.ModelForm):
    """
    Форма добавления статей на сайте
    """
    class Meta:
        model = Note
        fields = ('title', 'full_description', 'status')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',  'background-color':'red',
                'color': 'red',
                'autocomplete': 'off'
            })
