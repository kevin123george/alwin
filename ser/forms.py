from django import forms
from .models import Post,Quantity
from django.contrib.auth.models import User


class ser_req(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
    
class buy(forms.ModelForm):     #new
    class Meta:                 #new
        model = Quantity               #new
        fields = '__all__'           #new
    