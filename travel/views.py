from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile, Post
from django.template import loader
from travel.forms import AddUserForm, EditUserForm,AddArticalForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.urls import reverse

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

# def update_detail(request, member_id):
#     member_profile = get_object_or_404(UserProfile, member_id=member_id)
    
#     if request.method == 'POST':
#         form = EditUserForm(request.POST, instance=member_profile)
#         if form.is_valid():
#             updated_profile = form.save()
#             return HttpResponseRedirect(reverse('travel:personal', args=[member_id]))
#     else:
#         form = EditUserForm(instance=member_profile)
    
#     context = {'user': member_profile, 'form': form}
#     return render(request, 'update_detail.html', context)

def update_detail(request, member_id):
    member_profile = get_object_or_404(UserProfile, member_id=member_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=member_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', member_id=member_profile.member_id)
    else:
        form = EditUserForm(instance=member_profile)
    
    context = {'form': form}
    return render(request, 'update_detail.html', context)