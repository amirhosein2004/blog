from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm, CreateUserForm
from django.contrib.auth.models import User
from .models import Post, Topic



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    all_posts = Post.objects.all().count
    posts = Post.objects.filter(
        Q(topic__name__icontains=q)
    ).order_by('-created')
    topics = Topic.objects.all()[0:5]
    return render(request, 'blog/home.html', {'posts': posts, 'topics': topics, 'all_posts': all_posts})

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You login successfully')
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is wrong')
    return render(request, 'blog/login.html')

def Logout(request):
    logout(request)
    return redirect('home')

def Register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'].lower(), email=cd['email'], password=cd['password'])
            login(request, user)
            messages.success(request, 'You registered successfully')
            return redirect('home')

    return render(request, 'blog/register.html', {'form': form})

def PostPage(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, 'blog/postpage.html', {'post': post})

def TopicPage(request):
    topics = Topic.objects.all()
    return render(request, 'blog/topicpage.html', {'topics': topics})

@login_required(login_url='login')
def CreatePost(request):
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.host = request.user
            post.save()
            return redirect('home')
    return render(request, 'blog/createpost.html', {'form': form})

@login_required(login_url='login')
def UpdatePost(request, pk):
    post = Post.objects.get(id=pk)
    form = CreatePostForm(instance=post)
    if request.user != post.host:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post updated successfully')
            return redirect('home')
        else:
            messages.error(request, 'Entered information are invalid')
    return render(request, 'blog/updatepost.html', {'form': form})