from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Blog, Category, BlogImage, BlogVideo


# ==========================
# CKEditor Form for Blog
# ==========================
class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        fields = '__all__'


# ==========================
# Inline Models
# ==========================
class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    fields = ('image', 'caption',)
    readonly_fields = ()
    show_change_link = True


class BlogVideoInline(admin.TabularInline):
    model = BlogVideo
    extra = 1
    fields = ('video_file', 'video_url', 'caption',)
    readonly_fields = ()
    show_change_link = True


# ==========================
# Category Admin
# ==========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


# ==========================
# Blog Admin
# ==========================
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('title', 'author', 'category', 'created_at', 'views')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    inlines = [BlogImageInline, BlogVideoInline]

    fieldsets = (
        ('Main Information', {
            'fields': ('author', 'title', 'slug', 'category', 'image', 'content', 'tags')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('System Info', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ==========================
# Optional Separate Admin Views
# ==========================
# @admin.register(BlogImage)
# class BlogImageAdmin(admin.ModelAdmin):
#     list_display = ('blog', 'caption', 'image_preview')

#     def image_preview(self, obj):
#         if obj.image:
#             return f'<img src="{obj.image.url}" width="80" style="border-radius:6px;" />'
#         return "No image"
#     image_preview.allow_tags = True
#     image_preview.short_description = "Preview"


# @admin.register(BlogVideo)
# class BlogVideoAdmin(admin.ModelAdmin):
#     list_display = ('blog', 'caption', 'video_file', 'video_url')
