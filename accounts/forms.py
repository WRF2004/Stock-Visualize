from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UploadedFile

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None  
        self.fields['username'].label = "Username"  
        self.fields['password1'].help_text = None  
        self.fields['password1'].label = "Password"  
        self.fields['password2'].help_text = None  
        self.fields['password2'].label = "Re-enter password"  
class UploadFileForm(forms.Form):
    file = forms.FileField()
    class Meta:
        model = UploadedFile
        fields = ['file']