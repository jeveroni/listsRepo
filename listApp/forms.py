from django import forms
from .models import List, Item


class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ('name',)
        
class ListForm(forms.ModelForm):
    
    class Meta:
        model = List
        fields = ('name',)