from django import forms
from .models import User, UserProfile,Post, Tag
from django.contrib.auth.forms import UserCreationForm

class AddUserForm(UserCreationForm):

    email = forms.EmailField(label='Email', max_length=254)
    first_name = forms.CharField(label='First Name', max_length=30)
    last_name = forms.CharField(label='Last Name', max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class EditUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture', 'bio']
        labels = {
            'picture': '頭像',
            'bio': '個人簡介',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 80}),
        }

class AddArticalForm(forms.ModelForm):
   
    class Meta:
        model = Post     # 對應的資料
        fields = ['user', 'title', 'created_at', 'tags','description']
class EditArticalForm(forms.ModelForm):
   
    class Meta:
        model = Post     # 對應的資料
        fields = ['title','tags','description']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False, label='Tag')
    
