from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile, Post
from django.template import loader
from travel.forms import AddUserForm, EditUserForm,AddArticalForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.urls import reverse

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib import auth
from django.shortcuts import render

from .forms import LoginForm

def home(request):
    posts = Post.objects.all()
    template = loader.get_template('home.html')
    context = {
      'posts': posts
    }
    return HttpResponse(template.render(context, request))

def add_member(request):
    if request.method == 'GET':
        new_user = loader.get_template('add_membership.html')
        context = {'form': AddUserForm()}
        return HttpResponse(new_user.render(context, request))
    
def edit_article(request):
    return render(request, 'edit_article.html')

@login_required
def add_article(request, post_id):
  
    if request.user.is_authenticated:
        if request.method == 'GET':
            
            initial = {
                'post': post_id,
                'user': request.user,
                'created_at': date.today(),
                'title': '', 
                'tags': '',
                'description': ''}
            addarticalForm = AddArticalForm(initial)
            context = {'addarticalForm': addarticalForm}
            return render(request, 'add_artical.html', context)
        elif request.method == "POST":
           
            print (f"request.POST: {request.POST}")
            try:
                user = UserProfile.objects.get(user=request.user)
            except:
                print (f'{request.user} is not a member')
                pass
            addarticalForm = AddArticalForm(request.POST)
            if addarticalForm.is_valid():
                addarticalForm.save()
                print ('addartical successfully (saved)')
                result = 'Add ok'
            else:
                print ('Add fails (form is not valid)')
                result = 'Add fail'
            context = {
                'addarticalForm': addarticalForm,
                'result': result, 
                'user': user,
                'created_at': date.today()
            }    
            return render(request, 'add_result.html', context)
        
def post_detail(request, post_id):
    post = Post.objects.get( id=post_id)
    template = loader.get_template('post_detail.html')
    context = {
      'post': post
    }
    return HttpResponse(template.render(context, request))
    # return render(request, 'post_detail.html', context)

# {'post': post}


def detail(request, member_id):
    member_profile = get_object_or_404(UserProfile, member_id=member_id)
    return render(request, 'detail.html', {'user': member_profile})

def personal(request, member_id):
    member_profile = get_object_or_404(UserProfile, member_id=member_id)
    return render(request, 'personal.html', {'user': member_profile})

def update_detail(request, member_id):
    member_profile = get_object_or_404(UserProfile, member_id=member_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=member_profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('travel:personal', args=[member_id]))
    else:
        form = EditUserForm(instance=member_profile)
    
    context = {'form': form}
    return render(request, 'update_detail.html', context)

def login(request):
    login_page = loader.get_template('login.html')
    if request.method == 'GET':
        login_form = LoginForm()
        context = {
            'user': request.user,
            'login_form': login_form,
        }
        return HttpResponse(login_page.render(context, request))
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                main_page = loader.get_template('home.html')
                context = {'user': request.user,
                           'message': 'login ok'}
                return HttpResponse(login_page.render(context, request))
            else:
                message = 'Login failed (auth fail)'
        else:                    
            print ('Login error (login form is not valid)')
    else:
        print ('Error on request (not GET/POST)')


def logout(request):
    ''' 登出 '''
    auth.logout(request)
    main_html = loader.get_template('home.html')
    context = {'user': request.user}
    return HttpResponse(main_html.render(context, request))