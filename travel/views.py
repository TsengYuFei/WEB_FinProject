from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest,HttpResponseForbidden
from .models import UserProfile, Post,Picture
from django.template import loader
from travel.forms import AddUserForm, EditUserForm,AddArticleForm,PictureForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib import auth
from django.shortcuts import render

from .forms import LoginForm, SearchForm

from django.db.models import Q

def home(request):
    posts = Post.objects.all()
    template = loader.get_template('home.html')
    context = {
      'posts': posts
    }
    return HttpResponse(template.render(context, request))

def add_member(request):
    if request.method == 'GET':
        form = AddUserForm()
        return render(request, 'add_membership.html', {'form': form})

    elif request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            result = 'Add a new user successfully'
            return render(request, 'add_member_result.html', {'result': result})
        else:
            # Format the error messages
            errors = []
            for field, error_list in form.errors.items():
                for error in error_list:
                    errors.append(error)
            return render(request, 'add_membership.html', {'form': form, 'errors': errors})


def add_article(request):
    if request.method == 'GET':
        addarticleForm = AddArticleForm()
        pictureForm = PictureForm()
        context = {
            'addarticleForm': addarticleForm,
            'pictureForm': pictureForm
        }
        return render(request, 'add_article.html', context)

    elif request.method == 'POST':
        addarticleForm = AddArticleForm(request.POST)
        pictureForm = PictureForm(request.POST, request.FILES)

        if addarticleForm.is_valid() :
            post = addarticleForm.save(commit=False)
            post.user = request.user
            post.save()
            addarticleForm.save_m2m()

            if pictureForm.is_valid():

                files = request.FILES.getlist('picture')
                if files:
                    for file in files:
                        picture = Picture(picture=file)
                        picture.save()
                        post.pictures.add(picture)

                # picture = pictureForm.save(commit=False)
                # picture.save()
                # post.pictures.add(picture)
            else:
                context = {
                'addarticleForm': addarticleForm,
                'pictureForm': pictureForm,
                'result': 'Photo Add fail',
                'created_at': date.today()
                }
                return render(request, 'add_article_result.html', context)
            
            # return redirect('post_detail', post_id=post.id)

        else:
            context = {
                'addarticleForm': addarticleForm,
                'pictureForm': pictureForm,
                'result': 'Add fail',
                'created_at': date.today()
            }
        context = {
            'addarticleForm': addarticleForm,
            'pictureForm' : pictureForm,
            'result': '文章新增成功', 
            'created_at': date.today()
        }    
        return render(request, 'add_article_result.html', context)
    else:
        return HttpResponseBadRequest()
def edit_article(request, id):
    post = get_object_or_404(Post, id=id, user=request.user)

    if request.method == 'POST':
        form = AddArticleForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('travel:post_detail', id=post.id)
    else:
        form = AddArticleForm(instance=post)

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'edit_article.html', context)

def delete_article(request,id):        
    post = get_object_or_404(Post, id= id, user=request.user)
    if post.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        member_id = post.user.profile.member_id
        post.delete()
        return redirect(reverse('travel:personal', args=[member_id]))
    context = {
        'post': post
    }
    return render(request, 'delete_article.html',context)        
               
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    template = loader.get_template('post_detail.html')
    context = {
      'post': post,
    }
    return HttpResponse(template.render(context, request))
  


def detail(request, member_id):
    member_profile = get_object_or_404(UserProfile, member_id=member_id)
    posts = Post.objects.filter(user=member_profile.user)
    context = {
      'posts': posts,
      'user': member_profile,
    }
    return render(request, 'detail.html', context)

def personal(request, member_id):
    member_profile = get_object_or_404(UserProfile, member_id=member_id)
    posts = Post.objects.filter(user=member_profile.user)
    context = {
      'posts': posts,
      'user': member_profile,
    }
    return render(request, 'detail.html', context)

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
                home_page = loader.get_template('home.html') ##登入後導到home.html
                context = {'user': request.user,
                           'message': 'login ok'}
                return HttpResponse(home_page.render(context, request))
            else:
                message = 'Login failed (auth fail)'
        else:                    
            print ('Login error (login form is not valid)')
    else:
        print ('Error on request (not GET/POST)')


def logout(request):
    auth.logout(request)
    main_html = loader.get_template('home.html')
    context = {'user': request.user}
    return HttpResponse(main_html.render(context, request))

def search_posts(request):
    form = SearchForm(request.GET or None)
    posts = Post.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')

        if query:
            posts = posts.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

    return render(request, 'search_results.html', {'form': form, 'posts': posts})

from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})