from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('edit_article/', views.edit_article, name='edit_article'),
    path('post_detail/', views.post_detail, name='post_detail'),
    path('add_membership/', views.add_member, name = 'add_member'),
    path('<str:member_id>/detail/', views.detail, name = 'detail'),
]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
