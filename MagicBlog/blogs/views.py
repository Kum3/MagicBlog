from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Blog, User, Like, Comment

# Create your views here.
def index(request):
    """
    This view will deal with the entry point page of MagicBlog
    """
    return render(request=request, template_name="blogs\index.html")

def my_profile(request):
    user = User.objects.get(is_active=True)
    blogs = get_blogs({"created_by": user})
    context = {"blogs":blogs}
    return render(request=request, template_name="blogs\myprofile.html", context=context)

def detail(request):
    """
    This view will deal with the main page of MagicBlog
    """
    blogs = get_blogs()
    context_dict = {"blogs":blogs}
    return render(request=request, template_name="blogs\detail.html", context=context_dict)

def get_blogs(filters={}):
    blogs = Blog.objects.filter(**filters)
    return blogs

def login(request):
    """
    This view will deal with the login page of MagicBlog
    """
    username = request.POST.get("username")
    password = request.POST.get("password")
    if not username or not password:
        return render(request=request, template_name="blogs\login.html")
    try:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        sign_out_all_users(user.id)
    except User.DoesNotExist:
        raise Exception("No user exists from this username.")
    if user.password != password:
        raise Exception("Wrong password !!")
    return redirect("detail")

def sign_up(request):
    """
    This view will deal with the sign up page of MagicBlog
    """
    username = request.POST.get("username")
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    password = request.POST.get("password")
    email = request.POST.get("email")
    if not username and not firstname and not lastname and not password and not email:
        return render(request=request, template_name="blogs\signup.html")
    try:
        user = User.objects.create(username=username, first_name=firstname, last_name=lastname, password=password, email=email, is_active=True)
        sign_out_all_users(user.id)
    except Exception as e:
        raise Exception(e)
    return redirect("detail")

def blog(request, pk):
    comment = request.POST.get("comment")
    if not comment:
        try:
            blog = Blog.objects.get(pk=pk)
            user = User.objects.get(is_active=True)
            like_check = Like.objects.filter(blog=blog, user=user)
            liked = "UnLike" if like_check.count() > 0 else "Like"
        except Blog.DoesNotExist:
            raise Exception("Invalid Blog!")
        context = {"blog":blog, "liked":liked}
        return render(request=request, template_name="blogs\\blog.html", context=context)
    user = User.objects.get(is_active=True)
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        raise Exception("Invalid Blog!")
    Comment.objects.create(text = comment, blog=blog, user=user)
    return redirect("blog", pk=pk)

def like(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        raise Exception("Invalid Blog!")
    user = User.objects.get(is_active=True)
    like_check = Like.objects.filter(blog=blog, user=user)
    if like_check.count() > 0:
        like_check.delete()
        return redirect("blog", pk=pk)
    Like.objects.create(blog=blog, user=user)
    return redirect("blog", pk=pk)

def add_new_blog(request):
    summary = request.POST.get("summary")
    description = request.POST.get("description")
    if not summary and not description: 
        return render(request=request, template_name="blogs\\addblog.html")
    user = get_active_user()
    Blog.objects.create(summary=summary, description=description, created_by=user)
    return redirect("myprofile")
    

def sign_out_all_users(user_id):
    unactive_users = []
    users = User.objects.exclude(id=user_id)
    for user in users:
        user.is_active = False
        unactive_users.append(user)
    User.objects.bulk_update(unactive_users, ["is_active"])

def get_active_user():
    return User.objects.get(is_active=True)