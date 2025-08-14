from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Email ünvanınızı daxil edin'})
    )
    username = forms.CharField(
        label="İstifadəçi adı",
        widget=forms.TextInput(attrs={'placeholder': 'İstifadəçi adınızı daxil edin'})
    )
    password1 = forms.CharField(
        label="Şifrə",
        widget=forms.PasswordInput(attrs={'placeholder': 'Şifrənizi daxil edin'})
    )
    password2 = forms.CharField(
        label="Şifrə təsdiqi",
        widget=forms.PasswordInput(attrs={'placeholder': 'Şifrənizi təkrar daxil edin'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu email artıq qeydiyyatdan keçib.")
        return email
