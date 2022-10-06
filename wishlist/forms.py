from django import forms
from wishlist.models import BarangWishlist
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  

class BarangForm(forms.ModelForm):
    class Meta:
        model = BarangWishlist
        fields = ('nama_barang','harga_barang', 'deskripsi')

        widgets = {
            'nama_barang' : forms.TextInput(attrs={'class':'form-control'}),
            'harga_barang' : forms.TextInput(attrs={'class':'form-control'}), 
            'deskripsi' : forms.Textarea(attrs={'class':'form-control'})
        }
        