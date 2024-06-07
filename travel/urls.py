from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('', views.home, name = 'home'),
    # path('home/', views.home, name = 'home'),
    path('add_article/', views.add_article, name='add_article'),
    path('<int:post_id>/post_detail/', views.post_detail, name='post_detail'),
    path('add_membership/', views.add_member, name = 'add_member'),
    path('<str:member_id>/detail/', views.detail, name = 'detail'),
    path('<str:member_id>/personal/', views.personal, name = 'personal'),
    path('<str:member_id>/personal/edit/', views.update_detail, name = 'update_detail'),
]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
