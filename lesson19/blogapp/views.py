from _curses import flash
import datetime

from django.core.paginator import Paginator
from faker import Faker

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password
from .models import Posts


def home(request):

    posts_limit = 50
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    search = request.GET.get('search', '')
    date = request.GET.get('date')

    if search and date:
        start_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        end_date = start_date + datetime.timedelta(days=1)

        posts = Posts.objects.filter(title__contains=search, created__range=(start_date, end_date)).select_related('author')
    elif search:
        posts = Posts.objects.filter(title__contains=search).select_related('author')
    elif date:
        start_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        end_date = start_date + datetime.timedelta(days=1)

        posts = Posts.objects.filter(created__range=(start_date, end_date)).select_related('author')
    else:
        posts = Posts.objects.all().select_related('author')

    posts_paginator = Paginator(posts, posts_limit)

    if page > posts_paginator.num_pages:
        page = posts_paginator.num_pages
    if page < 1:
        page = 1

    return render(
        request, 'basic/home.html',
        {
            'posts': posts_paginator.page(page),
            'search': search,
            'date': date,
            'page': page,
            'num_pages': int(posts_paginator.num_pages)
        }
    )


@login_required(login_url='/')
def profile(request):
    return render(request, 'login/profile.html', {'name': request.user.first_name})


def show_post(request, post_id):
    post = Posts.objects.filter(id=post_id).get()
    if not post:
        Http404()
    return render(request, 'basic/post.html', {'post': post})


@login_required(login_url='/')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        messages = []
        if not title:
            messages.append('Title is required!')
        if not content:
            messages.append('Content is required!')

        if len(messages):
            return render(request, 'basic/create.html', {'messages': messages})

        Posts.objects.create(title=title, content=content, author=request.user)
        return redirect('home')

    return render(request, 'basic/create.html')


@login_required(login_url='/')
def edit_post(request, post_id):
    post = Posts.objects.filter(id=post_id).get()
    title = post.title

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')

        messages = []
        if not post.title:
            messages.append('Title is required!')
        if not post.content:
            messages.append('Content is required!')

        if len(messages):
            return render(request, 'basic/edit.html', {'post': post, 'messages': messages, 'title': title})

        post.save()
        return redirect('show_post', post_id=post.id)

    return render(request, 'basic/edit.html', {'post': post, 'title': title})


@login_required(login_url='/')
def delete_post(request, post_id):
    post = Posts.objects.filter(id=post_id).get()
    post.delete()
    # messages = [f'"{post.title}" was successfully deleted!']
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')

        user_email = User.objects.filter(email=email).first()
        user_name = User.objects.filter(username=username).first()

        messages = []
        if not (email and username and first_name and password):
            messages.append('All fields must be filled')
            return render(request, 'login/signup.html', {'messages': messages})

        if user_email or user_name:  # if a user is found, we want to redirect back to signup page so user can try again
            messages.append('A user with this email or username already exists')
            return render(request, 'login/signup.html', {'messages': messages})

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        User.objects.create(email=email, username=username, first_name=first_name, password=make_password(password))
        return redirect('login')

    return render(request, 'login/signup.html')


def create_fake_posts(request):
    """

    :type request: object
    """
    faker_ = Faker('ru_RU')

    posts = []
    for i in range(340):
        posts.append(
            Posts(title=faker_.sentence(nb_words=5),
                  content=faker_.sentence(nb_words=50),
                  author=User.objects.order_by("?").first())
        )

    Posts.objects.bulk_create(posts)

    return redirect('home')
