from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Item

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_type', 'name', 'description', 'location', 'contact_info', 'image']
        widgets = {
            'item_type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Blue Water Bottle'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide details like brand, color, etc.'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Library, 2nd Floor'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your email or phone number'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }