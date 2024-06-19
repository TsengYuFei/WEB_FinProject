from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest,HttpResponseForbidden
from .models import UserProfile, Post,Picture, Tag
from django.template import loader
from travel.forms import AddUserForm, EditUserForm,AddArticleForm
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

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages




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
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            profile = UserProfile(
                user=user,
                picture=form.cleaned_data['picture'],
                bio=form.cleaned_data['bio']
            )
            profile.save()            
            result = '註冊成功！'
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
        context = {
            'addarticleForm': addarticleForm,
        }
        return render(request, 'add_article.html', context)

    elif request.method == 'POST':
        addarticleForm = AddArticleForm(request.POST, request.FILES)

        if addarticleForm.is_valid():
            post = addarticleForm.save(commit=False)
            post.user = request.user
            post.save()

            # Handle file uploads
            if request.FILES.getlist('pictures'):
                for picture in request.FILES.getlist('pictures'):
                    print("Picture content:", picture)
                    picture_instance = Picture.objects.create(picture=picture)
                    post.pictures.add(picture_instance)

            tags = addarticleForm.cleaned_data['tags']
            if tags:
                tag_names = [tag.strip() for tag in tags.split(',')]
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    post.tags.add(tag)
                    
            # context = {
            #     'addarticleForm': addarticleForm,
            #     'result': '文章新增成功',
            #     'created_at': date.today()
            # }
            member_id = request.user.profile.member_id
            return redirect(reverse('travel:personal', args=[member_id]))
            # return render(request, 'add_article_result.html', context)
        else:
            context = {
                'addarticleForm': addarticleForm,
                'result': 'Add fail',
                'created_at': date.today()
            }
            return render(request, 'add_article_result.html', context)

    else:
        return HttpResponseBadRequest()
    
def edit_article(request, id):
    post = get_object_or_404(Post, id=id, user=request.user)

    if request.method == 'POST':
        form = AddArticleForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            if request.FILES.getlist('pictures'):
                for picture in request.FILES.getlist('pictures'):
                    print("Picture content:", picture)
                    picture_instance = Picture.objects.create(picture=picture)
                    post.pictures.add(picture_instance)
            post.save()
            return redirect('travel:post_detail', id=post.id)
    else:
        form = AddArticleForm(instance=post)

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'edit_article.html', context)

def delete_picture(request):
    if request.method == 'POST':
        picture_ids = request.POST.getlist('delete_pictures')
        if picture_ids:
            Picture.objects.filter(id__in=picture_ids).delete()
        return redirect(request.META.get('HTTP_REFERER'))

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
    return render(request, 'personal.html', context)

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
                #home_page = loader.get_template('travel:home') ##登入後導到home.html
                # context = {'user': request.user,
                #            'message': 'login ok'}
                # return HttpResponse(home_page.render(context, request))
                return redirect('travel:home')
            else:
                login_form.add_error(None, '輸入的帳號或密碼錯誤')
                context = {'login_form': login_form}
                return render(request, 'login.html', context)
                # message = 'Login failed (auth fail)'
        else:                    
            print ('Login error (login form is not valid)')
    else:
        print ('Error on request (not GET/POST)')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth_login(request, user)
#             return redirect('travel:home')  # Redirect to home page after successful login
#         else:
#             login_form = LoginForm(request.POST)
#             messages.error(request, 'Invalid username or password')
#             login_form.add_error(None, '輸入的帳號或密碼錯誤')
#     return render(request, 'login.html', {'login_form': LoginForm()})

def logout(request):
    auth_logout(request)
    #main_html = loader.get_template('home.html')
    #context = {'user': request.user}
    return redirect('travel:home')
#   return HttpResponse(main_html.render(context, request))

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