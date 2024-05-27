from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
#user: 與 Django 的 User 模型形成一對一關係。
# profile_picture: 儲存用戶的頭像圖片。
# bio: 用戶的個人簡介。

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='experiences')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
# user: 與 User 模型形成外鍵關係，表示這個經驗是由哪個用戶創建的。
# title: 經驗的標題。
# description: 經驗的詳細描述。
# tags: 與 Tag 模型形成多對多關係，允許每個經驗有多個標籤。
# created_at: 創建經驗的時間。

class Photo(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.experience.title}"
# experience: 與 Experience 模型形成外鍵關係，表示這張照片屬於哪個經驗。
# image: 照片文件，儲存在 uploads/ 目錄中。
# uploaded_at: 照片上傳的時間，自動設置為當前時間。