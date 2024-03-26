from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('post/<str:pk>', views.PostPage, name='postpage'),
    path('topicpage/', views.TopicPage, name='topicpage'),
    path('createpost/', views.CreatePost, name='createpost'),
    path('updatepost/<str:pk>/', views.UpdatePost, name='updatepost'),

    path('register/', views.Register, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
]