from django import forms
from .models import User, UserProfile,Post,Picture
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.password_validation import validate_password, UserAttributeSimilarityValidator, MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User


class AddUserForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        max_length=150,
        help_text='請輸入150個字符以內的用戶名(字母、數字、@/./+/-/_組成)',
        error_messages={
            'required': '請輸入用戶名',
        }
    )
    email = forms.EmailField(
        label='Email',
        max_length=254,
        error_messages={
            'required': '請輸入您的電子郵件地址',
            'invalid': '請輸入有效的電子郵件地址'
        }
    )
    first_name = forms.CharField(
        label='First Name',
        max_length=30,
        error_messages={
            'required': '請輸入您的名字'
        }
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=30,
        error_messages={
            'required': '請輸入您的姓氏'
        }
    )
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput,
        error_messages={
            'required': '請輸入密碼',
            
        },
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        strip=False,
        help_text='請再次輸入密碼以進行確認。',
        error_messages={
            'required': '請確認您的密碼',
        },
    )
    # email = forms.EmailField(label='Email', max_length=254)
    # first_name = forms.CharField(label='First Name', max_length=30)
    # last_name = forms.CharField(label='Last Name', max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_password2(self):
        # Override this method to remove password validation
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(user=user)  # 创建 UserProfile 实例
        return user

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

class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title here', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter your description here', 'class': 'form-control'}),
        }

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['picture']
        widgets = {
            'picture': forms.ClearableFileInput(attrs={'multiple': False}),
        }
        
class EditArticleForm(forms.ModelForm):
   
    class Meta:
        model = Post     # 對應的資料
        fields = ['title','description']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    
