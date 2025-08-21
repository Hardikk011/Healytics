from django.contrib import admin
from .models import UserProfile, Prediction, Medicine, Blog, BlogBookmark, Contact

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    list_filter = ['created_at']

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'predicted_cancer_type', 'confidence_score', 'created_at']
    list_filter = ['predicted_cancer_type', 'created_at']
    search_fields = ['user__username', 'predicted_cancer_type']
    readonly_fields = ['created_at']

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'generic_name', 'prediction', 'manufacturer']
    list_filter = ['created_at']
    search_fields = ['name', 'generic_name', 'manufacturer']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'views', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'tags': ('title',)}

@admin.register(BlogBookmark)
class BlogBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'blog__title']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
