# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('edit_article/', views.edit_article, name='edit_article'),
    # 其他路由設置...
]
