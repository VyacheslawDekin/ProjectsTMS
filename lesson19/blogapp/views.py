from _curses import flash
import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.views import Response, APIView
from rest_framework import permissions

from django.views.decorators.csrf import csrf_exempt
from faker import Faker

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.hashers import make_password
from .models import Posts
from django.shortcuts import get_object_or_404
from .serializers import PostsSerialiser, PostsPermission, UsersSerializer, UserCreateSerializer


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

        query = Q(title__contains=search) | Q(content__contains=search)
        query &= Q(created__range=(start_date, end_date))

        posts = Posts.objects.filter(query).select_related(
            'author') \
            .values('id', 'title', 'content', 'created', 'author__username')
    elif search:
        query = Q(title__contains=search) | Q(content__contains=search)
        posts = Posts.objects.filter(query).select_related('author') \
            .values('id', 'title', 'content', 'created', 'author__username')
    elif date:
        start_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        end_date = start_date + datetime.timedelta(days=1)

        posts = Posts.objects.filter(created__range=(start_date, end_date)) \
            .select_related('author') \
            .values('id', 'title', 'content', 'created', 'author__username')
    else:
        posts = Posts.objects.all().select_related('author') \
            .values('id', 'title', 'content', 'created', 'author__username')

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


@api_view(['GET', 'POST'])
def posts_api(request):
    if request.method == "GET":
        posts = Posts.objects.all()[:50]
        serializer = PostsSerialiser(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST" and not request.user.is_anonymous:
        serializer = PostsSerialiser(data=request.data)
        print(request.data)
        if serializer.is_valid():
            author = request.user
            created = datetime.datetime.now()
            serializer.save(author=author, created=created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'detail': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
def post_api_detail(request, pk):
    post = get_object_or_404(Posts, id=pk)

    if request.method == "GET":
        serializer = PostsSerialiser(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT" and not request.user.is_anonymous:
        serializer = PostsSerialiser(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE" and not request.user.is_anonymous:
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response({'detail': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


class PostsViewApi(APIView):

    def get(self, request):
        posts = Posts.objects.all()[:50]
        serializer = PostsSerialiser(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_anonymous:
            return Response({'detail': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PostsSerialiser(data=request.data)
        print(request.data)
        if serializer.is_valid():
            author = request.user
            created = datetime.datetime.now()
            serializer.save(author=author, created=created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if request.user.is_anonymous:
            return Response({'detail': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        post = get_object_or_404(Posts, id=pk)

        serializer = PostsSerialiser(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.is_anonymous:
            return Response({'detail': 'not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        post = get_object_or_404(Posts, id=pk)
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PostsListCreateApiView(generics.ListCreateAPIView):
    serializer_class = PostsSerialiser
    queryset = Posts.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        created = datetime.datetime.now()
        serializer.save(author=self.request.user, created=created)


    def get_queryset(self):
        query = Q()

        if self.request.GET.get("date"):
            date = self.request.GET.get("date")
            start_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            end_date = start_date + datetime.timedelta(days=1)

            query = Q(created__range=(start_date, end_date))

        if self.request.GET.get("search"):
            search = self.request.GET.get("search")
            query &= Q(title__contains=search) | Q(content__contains=search)

        posts = Posts.objects.filter(query).select_related('author') \
            .values('id', 'title', 'content', 'created', 'author__username')

        return posts


class PostsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostsSerialiser
    queryset = Posts.objects.all()
    permission_classes = [PostsPermission]
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UsersSerializer

        return UserCreateSerializer


