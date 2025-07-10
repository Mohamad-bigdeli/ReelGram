from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_verified', 'is_staff', 'is_superuser', 'created_at')
    list_filter = ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('id', 'created_at', 'updated_at', 'last_login')
    
    def get_object(self, request, object_id, from_field=None):
        return super().get_object(request, object_id, from_field)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'birth_date', 'follower_count', 'following_count', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'full_name')
    ordering = ('-created_at',)
    fieldsets = (
        (_('User Info'), {
            'fields': ('user', 'full_name', 'bio', 'birth_date')
        }),
        (_('Media'), {
            'fields': ('profile_picture',)
        }),
        (_('Stats'), {
            'fields': ('follower_count', 'following_count'),
            'classes': ('collapse',)
        }),
        (_('Dates'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'follower_count', 'following_count')
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" width="50" height="50" style="border-radius: 50%;" />'
        return 'No Image'
    profile_picture_preview.allow_tags = True
    profile_picture_preview.short_description = 'Picture'
    list_display = ('user', 'full_name', 'profile_picture_preview', 'follower_count', 'following_count', 'created_at')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fields = ('full_name', 'bio', 'birth_date', 'profile_picture')
