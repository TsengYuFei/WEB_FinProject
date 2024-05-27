from django.contrib import admin
from .models import UserProfile, Tag, Experience, Photo

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)

class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "user")

class PhotoAdmin(admin.ModelAdmin):
    list_display = ("experience", "uploaded_at")

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Experience,ExperienceAdmin)
admin.site.register(Photo,PhotoAdmin)