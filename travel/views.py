from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile, Post, Tag, User
from django.template import loader
from travel.forms import AddUserForm, EditUserForm
from django.urls import reverse

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

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {'post': post})

def detail(request, member_id):
    member_profile = get_object_or_404(UserProfile, member_id=member_id)
    return render(request, 'detail.html', {'user': member_profile})

def personal(request, member_id):
    member_profile = get_object_or_404(UserProfile, member_id=member_id)
    return render(request, 'personal.html', {'user': member_profile})

def update_detail(request, member_id):
    member_profile = get_object_or_404(UserProfile, member_id=member_id)
    
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=member_profile)
        if form.is_valid():
            updated_profile = form.save()
            return HttpResponseRedirect(reverse('travel:personal', args=[member_id]))
    else:
        form = EditUserForm(instance=member_profile)
    
    context = {'user': member_profile, 'form': form}
    return render(request, 'update_detail.html', context)