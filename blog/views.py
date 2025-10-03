from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Users, Post, Comment

# Create your views here.

def login_required(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        return redirect('login')


def home(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    try:
        user = Users.objects.get(id=request.session['user_id'])
        posts = Post.objects.filter(author__in=user.following.all()).order_by('-created_at')[:5]
        # If no posts from following, show all recent posts
        if not posts:
            posts = Post.objects.all().order_by('-created_at')[:5]
    except Users.DoesNotExist:
        return redirect('login')
    return render(request, 'blog/home.html', {'posts': posts, 'user': user})


def explore(request):
    posts = Post.objects.all().order_by('-created_at')
    try:
        user = Users.objects.get(id=request.session['user_id']) if 'user_id' in request.session else None
    except Users.DoesNotExist:
        return redirect('login')
    if request.method == 'GET':
        search_query = request.GET.get('q', '')
        posts = posts.filter(title__icontains=search_query)  # Simple search by title
        

    return render(request, 'blog/explore.html', {'posts': posts, 'user': user})


def postView(request, id):
    login_required(request)
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post)
    number_of_comments = comments.count()
    content = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'blog/postView.html', content)



def deletePost(request, post_id):
    login_required(request)
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponse("Post does not exist")

    if post.author.id != request.session['user_id']:
        return HttpResponse("You are not authorized")

    post.delete()
    return redirect('profile')


def add_comment(request, post_id):
    login_required(request)
    if request.method =='POST':
        post = Post.objects.get(id=post_id)
        content = request.POST.get('content')
        author = Users.objects.get(id=request.session['user_id'])  # Assuming user is logged in and user_id is stored in session
        comment = Comment(post=post, author=author, content=content)
        comment.save()
        post.allComments.add(comment)
        post.save()
        return redirect('postView', id=post_id)
    return HttpResponse("Invalid request method.")


def follow_user(request, user_id):
    login_required(request)
    try:
        user_to_follow = Users.objects.get(id=user_id)
        current_user = Users.objects.get(id=request.session['user_id'])
    except Users.DoesNotExist:
        return HttpResponse("User does not exist")

    if user_to_follow != current_user:
        if user_to_follow in current_user.following.all():
            current_user.following.remove(user_to_follow)
            user_to_follow.followers.remove(current_user)

        else:
            current_user.following.add(user_to_follow)
            user_to_follow.followers.add(current_user)
        current_user.save()
    return redirect('viewProfile', user_id=user_id)


def viewProfile(request, user_id):
    login_required(request)
    is_authenticated = 'user_id' in request.session

    if user_id == request.session.get('user_id'):
        return redirect('profile')
    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return HttpResponse("User does not exist")
    user_posts = user.posts.all()
    comments_count = Comment.objects.filter(author=user).count()
    target_user = Users.objects.get(id=user_id)
    followed_by_current_user = False
    if target_user in Users.objects.get(id=request.session['user_id']).following.all():
        followed_by_current_user = True

    return render(request, 'blog/viewProfile.html', {'user': user, 'posts': user_posts, 'comments_count': comments_count, 'is_authenticated': is_authenticated, 'followed_by_current_user': followed_by_current_user})



def profile(request):
    login_required(request)
    is_authenticated = 'user_id' in request.session
    try:
        user = Users.objects.get(id=request.session['user_id'])
    except Users.DoesNotExist:
        return redirect('login')
    user_posts = user.posts.all()
    comments_count = Comment.objects.filter(author=user).count()
    return render(request, 'auth/profile.html', {'user': user, 'posts': user_posts, 'comments_count': comments_count, 'is_authenticated': is_authenticated})


def edit_profile(request):
    login_required(request)
    try:
        user = Users.objects.get(id=request.session['user_id'])
    except Users.DoesNotExist:
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('avatar')

        if Users.objects.filter(username=username).exists() and username != user.username:
            return HttpResponse("Username already taken")

        user.name = name
        user.username = username
        user.bio = bio
        if profile_picture:
            user.profile_picture = profile_picture
        user.save()
        return redirect('profile')
    return render(request, 'auth/editProfile.html', {'user': user})

def remove_profile_picture(request):
    login_required(request)
    try:
        user = Users.objects.get(id=request.session['user_id'])
    except Users.DoesNotExist:
        return redirect('login')
    if user.profile_picture != "profile_pics/default_profile_picture.jpeg":
        user.profile_picture.delete(save=True)
        user.profile_picture = "profile_pics/default_profile_picture.jpeg"
        user.save()
    return redirect('edit_profile')

def createPost(request):
    login_required(request)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = Users.objects.get(id=request.session['user_id'])
        post = Post(title=title, content=content, author=author)
        post.save()
        Users.objects.get(id=request.session['user_id']).posts.add(post)
        return redirect('profile')
    return render(request, 'auth/createPost.html')


def login(request):
    if request.method == 'POST':
        # Handle login logic here
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if Users.objects.filter(username=username, password=password).exists():
            user = Users.objects.get(username=username)
            # Set session or cookie here for logged-in user
            request.session['user_id'] = user.id
            return redirect('home')
    return render(request, 'auth/login.html')


def register(request):
    if request.method == 'POST':
        # Handle registration logic here
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        profile_picture = "profile_pics/default_profile_picture.jpeg"

        if password1 != password2:
            return HttpResponse("Passwords do not match")
        if Users.objects.filter(username=username).exists():
            return HttpResponse("Username already taken")
        if Users.objects.filter(email=email).exists():
            return HttpResponse("Email already registered")
        user = Users(username=username, email=email, password=password1, profile_picture=profile_picture)
        user.save()
        return redirect('login')
    return render(request, 'auth/register.html')




def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')