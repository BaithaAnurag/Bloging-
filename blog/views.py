from django.shortcuts import render, get_object_or_404,redirect
from .models import Blog, Category, Comment
from django.core.paginator import Paginator
from taggit.models import Tag
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import CommentForm


def home(request):
    page_obj = Blog.objects.order_by('-created_at')[:10]  # your main paginated list
    recent_blogs = Blog.objects.order_by('-created_at')[:4]  # 4 recent posts for homepage
    latest_posts = Blog.objects.order_by('-created_at')[:5]
    trending_posts = Blog.objects.order_by('-views')[:5]
    tags = Tag.objects.all()

    context = {
        'page_obj': page_obj,
        'recent_blogs': recent_blogs,
        'latest_posts': latest_posts,
        'trending_posts': trending_posts,
        'tags': tags,
    }
    return render(request, 'home.html', context)


def About(request):
    return render(request,'about.html')


def Privacy(request):
    return render(request, 'privacy.html')


def Terms(request):
    return render(request,"terms.html")






def blog_list(request):
    query = request.GET.get("q")
    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")

    blogs = Blog.objects.all().order_by("-created_at")

    if query:
        blogs = blogs.filter(Q(title__icontains=query) | Q(content__icontains=query))

    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)

    if tag_slug:
        blogs = blogs.filter(tags__slug=tag_slug)

    paginator = Paginator(blogs, 6)  # 6 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Sidebar data
    latest_posts = Blog.objects.order_by("-created_at")[:5]
    trending_posts = Blog.objects.order_by("-views")[:5]
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "latest_posts": latest_posts,
        "trending_posts": trending_posts,
        "tags": tags,
        "query": query,
    }
    return render(request, "blog_list.html", context)


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    related_posts = Blog.objects.filter(category=blog.category).exclude(id=blog.id)[:4]
    comments = Comment.objects.filter(blog=blog).order_by('-created_at')

    next_post = Blog.objects.filter(id__gt=blog.id).order_by('id').first()
    previous_post = Blog.objects.filter(id__lt=blog.id).order_by('-id').first()

    # AJAX POST
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            return JsonResponse({'success': True, 'name': comment.name, 'text': comment.text})
        return JsonResponse({'success': False, 'errors': form.errors})

    context = {
        'blog': blog,
        'related_posts': related_posts,
        'comments': comments,
        'next_post': next_post,
        'previous_post': previous_post,
    }
    return render(request, 'blog_details.html', context)









@csrf_exempt
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if not all([name, email, subject, message]):
            return JsonResponse({"success": False, "message": "All fields are required."})

        # Format email content
        admin_message = f"""
        📩 New message from AI & Tech Blog Contact Form:
        ----------------------------
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message:
        {message}
        """

        try:
            send_mail(
                f"[AI & Tech Blog] {subject}",
                strip_tags(admin_message),
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # Admin email
                fail_silently=False,
            )
            return JsonResponse({"success": True, "message": "Thank you for contacting us!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error sending message: {str(e)}"})

    return render(request, "contact.html")