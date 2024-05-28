from django.urls import path
from . import views

urlpatterns = [
    path('edit_article/', views.edit_article, name='edit_article'),
    path('', views.home, name = 'home'),
    path('membership/', views.add_member, name = 'add_member'),
]
