# from django import forms
# from .models import Author, Product, User
# from django.core.exceptions import ValidationError
# from django.contrib.auth import get_user_model, authenticate

# class RegisterForm(forms.ModelForm):

   
#     password = forms.CharField(widget=forms.PasswordInput, max_length=16, required=True)
#     password_confirm = forms.CharField(widget=forms.PasswordInput, max_length=16, required=True)

#     class Meta:
#         model = User
#         fields = "__all__"


    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({"class": "form-control"})
#             # self.fields[field].required = True


#     # XSS temizlik ucun
#     def clean(self):
#         username = self.cleaned_data.get("username")
#         password = self.cleaned_data.get("password")
#         password_confirm = self.cleaned_data.get("password_confirm")


#         # Validatorlar ucun 
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError("This username is already exists")
        
#         if len(password) < 8:
#             raise forms.ValidationError("Minimum length is 8 symbols")
        
#         if password != password_confirm:
#             raise forms.ValidationError("Passwords dont match")
        
#         return self.cleaned_data



