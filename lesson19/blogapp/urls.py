from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='login/login.html'), name='login'),
    path('signup', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/', views.show_post, name='show_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('profile/', views.profile, name='profile'),

    #Fake
    path('create-fakeposts/', views.create_fake_posts, name='create_fake_posts'),

    #API
    path('posts-api', views.posts_api),
    path('posts-api/<int:pk>', views.post_api_detail),

    #API v2
    path('posts-api/v2', views.PostsViewApi.as_view()),
    path('posts-api/v2/<int:pk>', views.PostsViewApi.as_view()),

    #API view v3
    path('posts-api/v3', views.PostsListCreateApiView.as_view()),
    path('posts-api/v3/<int:pk>', views.PostsRetrieveUpdateDestroyAPIView.as_view()),

    path('users-api/v3', views.UserListCreateAPIView.as_view()),
    path('users-api/v3/<username>', views.PostsRetrieveUpdateDestroyAPIView.as_view()),
]


