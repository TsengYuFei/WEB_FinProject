from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import UserProfile, Experience, Tag, User
from django.template import loader
from travel.forms import AddUserForm

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def add_member(request):
    if request.method == 'GET':
        new_user = loader.get_template('add_membership.html')
        context = {'form': AddUserForm()}
        return HttpResponse(new_user.render(context, request))
    
def edit_article(request):
    return render(request, 'edit_article.html')

def detail(request, user_name):
    user = get_object_or_404(User, user_name=UserProfile.user.username)
    return (request, 'detail.html', {'user': user})