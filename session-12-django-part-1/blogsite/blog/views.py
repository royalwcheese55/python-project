from django.shortcuts import render, HttpResponse, Http404, get_object_or_404
from blog.models import Post, Category, Comment
from django.contrib.auth.models import User
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published=True).all()
    # return HttpResponse(f'List view {posts.count()}')
    context = {
        'posts': posts
    }
    return render(request, 'index.html', context)

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    if not post:
        raise Http404("Not found")
    comments = post.comments.all()
    context = {
        'post': post,
        'comments': comments
    }

    return render(request, 'post_detail.html', context)

def category_post(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = category.posts.filter(published=True).prefetch_related('categories', 'author')
    # for post in posts: #n+1 problem to prefetch to resolve
    #     post.author()

    context = {
        'posts': posts,
        'category': category
    }
    return render(request, 'category_posts.html', context)

def author_post(request, author_id):
    user = get_object_or_404(User, id=author_id)
    posts = user.posts.filter(published=True).prefetch_related('categories')
    context = {
        'posts': posts,
        'author': user
    }
    return render(request, 'author_posts.html', context)