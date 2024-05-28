from django.contrib import admin
from .models import UserProfile, Tag, Experience, Photo, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import AddUserForm

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    add_form = AddUserForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

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
# 取消註冊內建的 UserAdmin 並重新註冊自定義的 UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)