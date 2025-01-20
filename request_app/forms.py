from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError


class UserForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label='Возраст', max_value=100, min_value=1)
    info = forms.CharField(label='Информация', widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError('Файл содержит слово "Вирус"')



class UploadFileForm(forms.Form):
    file=forms.FileField(
        validators=[validate_file_name]
    )
