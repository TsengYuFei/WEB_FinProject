from django.shortcuts import render
from django.http import JsonResponse
from models import Experience, Tag

def edit_article(request):
    return render(request, 'edit_article.html')
