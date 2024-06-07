from django.contrib import admin
from .models import UserProfile, Post, User, Picture
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

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "user")



admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Post,PostAdmin)

admin.site.register(Picture)
# 取消註冊內建的 UserAdmin 並重新註冊自定義的 UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)