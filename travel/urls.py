from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('edit_article/', views.edit_article, name='edit_article'),
    path('add_membership/', views.add_member, name = 'add_member'),
    path('<str:member_id>/detail/', views.detail, name = 'detail'),
]
