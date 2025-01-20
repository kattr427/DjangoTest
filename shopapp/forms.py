from django import forms
from django.core import validators
from django.contrib.auth.models import Group

from .models import Product


#class ProductForm(forms.Form):
#    name=forms.CharField(label='Название',max_length=100)
#    price=forms.DecimalField(label='Цена', max_value=10000, min_value=1, decimal_places=2)
#    description=forms.CharField(
#        label='Описание товара',
#        widget=forms.Textarea(attrs={'rows': 5, 'cols': 30}),
#        validators=[validators.RegexValidator(
#            regex=r'новый',
#            message='Необходимо слово "новый"',
#        )]
#    )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name','price','description','discount'



class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']