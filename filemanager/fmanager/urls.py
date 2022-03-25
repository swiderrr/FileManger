from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('logincheck', views.login_check, name='login_check'),
    path('homepage', views.home_page, name='home_page'),
    path('logout', views.log_out, name='log_out'),
    path('signup', views.sign_up, name='signup_page'),
    path('postsignup', views.post_sign_up, name='post_sign_up'),
    path('addfile', views.add_file, name='add_file'),
    path('postfile', views.post_file, name='post_file'),
    path('file_edit/<filename>', views.file_edit, name='file_edit'),
]