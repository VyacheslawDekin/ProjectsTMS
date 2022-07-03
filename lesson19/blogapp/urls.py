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
]


