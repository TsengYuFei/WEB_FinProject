#還要加一下not NULL

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="用戶")
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, verbose_name="用戶頭像")
    bio = models.TextField(max_length=500, blank=True, verbose_name="個人簡介")

    def __str__(self):
        return self.user.username
        
    #user: 與 Django 的 User 模型形成一對一關係。

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="標籤")

    def __str__(self):
        return self.name
    
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences', verbose_name="發文者")
    title = models.CharField(max_length=255, verbose_name="文章標題")
    description = models.TextField(verbose_name="旅遊經驗")
    tags = models.ManyToManyField(Tag, related_name='experiences', verbose_name="標籤")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="旅遊日期")

    def __str__(self):
        return self.title
    
    # user: 與 User 模型形成外鍵關係，表示這個經驗是由哪個用戶創建的。
    # tags: 與 Tag 模型形成多對多關係，允許每個經驗有多個標籤。

class Photo(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='photos', verbose_name="文章")
    image = models.ImageField(upload_to='uploads/', verbose_name="照片", null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上傳時間")

    def __str__(self):
        return f"Photo for {self.experience.title}"
    
    # experience: 與 Experience 模型形成外鍵關係，表示這張照片屬於哪個經驗。
    # image: 照片文件，儲存在 uploads/ 目錄中。
    # uploaded_at: 照片上傳的時間，自動設置為當前時間。