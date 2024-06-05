from django import forms
from .models import User, UserProfile,Post
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
        fields = ['bio']
        labels = {'bio': ''}
        widgets = {'bio': forms.Textarea(attrs={'cols': 80})}

class AddArticalForm(forms.ModelForm):
   
    class Meta:
        model = Post     # 對應的資料
        fields = ['user', 'title', 'created_at', 'tags','description']
class EditArticalForm(forms.ModelForm):
   
    class Meta:
        model = Post     # 對應的資料
        fields = ['title','tags','description']
    