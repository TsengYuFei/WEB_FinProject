import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="用戶")
    picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, verbose_name="用戶頭像", help_text="請上傳1:1圖片", default="{% static 'picture/defult_head.png' %}")
    bio = models.TextField(max_length=500, blank=True, verbose_name="個人簡介")
    #會員編號自動生成(10位)不用輸入
    member_id = models.CharField(max_length=10, unique=True, verbose_name="會員編號", blank=True, help_text="系統將自動生成十碼會員編號")

    def save(self, *args, **kwargs):
        if not self.member_id:
            self.member_id = self.generate_unique_member_id()
        super(UserProfile, self).save(*args, **kwargs)

    def generate_unique_member_id(self):
        while True:
            member_id = ''.join(random.choices('0123456789', k=10))
            if not UserProfile.objects.filter(member_id=member_id).exists():
                return member_id

    def __str__(self):
        return self.user.username
        
    #user: 與 Django 的 User 模型形成一對一關係。

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="標籤")

    def __str__(self):
        return self.name
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="發文者")
    title = models.CharField(max_length=10, verbose_name="文章標題")
    description = models.TextField(verbose_name="文章內容")
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name="標籤")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="發文時間")
    # photo = models.ImageField(upload_to='Post_photos/', null=True, blank=True)

    def __str__(self):
        return self.title

class Post_Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos', verbose_name="文章")
    image = models.ImageField(upload_to='uploads/', verbose_name="照片", null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上傳時間")

    def __str__(self):
        return f"Photo for {self.post.title}"