from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from bs4 import BeautifulSoup


# =====================
# Category Model
# =====================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# =====================
# Blog Model
# =====================
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="blog_images/main/", blank=True, null=True)
    content = RichTextUploadingField()
    tags = TaggableManager(blank=True)

    # SEO fields
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)

    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # === Auto Slug and Alt Tags ===
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Parse CKEditor content to add alt/aria-labels automatically
        if self.content:
            soup = BeautifulSoup(self.content, 'html.parser')

            # Add alt for images
            for img in soup.find_all('img'):
                if not img.get('alt'):
                    img['alt'] = self.title

            # Add aria-label for videos
            for video in soup.find_all('video'):
                if not video.get('aria-label'):
                    video['aria-label'] = self.title

            # Add title for iframes (YouTube embeds)
            for iframe in soup.find_all('iframe'):
                if not iframe.get('title'):
                    iframe['title'] = self.title

            self.content = str(soup)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# =====================
# Blog Image Model
# =====================
class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog_images/multiple/')
    caption = models.CharField(max_length=255, blank=True)

    @property
    def alt_text(self):
        # Fallback to caption or blog title
        return self.caption or self.blog.title

    def __str__(self):
        return f"Image for {self.blog.title}"


# =====================
# Blog Video Model
# =====================
class BlogVideo(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='blog_videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="You can also paste a YouTube or Vimeo link")
    caption = models.CharField(max_length=255, blank=True)

    @property
    def alt_text(self):
        # Fallback to caption or blog title
        return self.caption or self.blog.title

    def __str__(self):
        return f"Video for {self.blog.title}"


class Comment(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.title}"