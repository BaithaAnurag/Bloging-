from django.urls import path,include
from django.conf import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),
    path("blogs/", views.blog_list, name="blog_list"),
    path("blogs/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('contact/', views.contact, name="contact"),
    path('about/',views.About, name="about"),
    path('privacy/',views.Privacy,name="privacy"),
    path('terms/',views.Terms,name="Terms"),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)