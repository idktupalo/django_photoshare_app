from django.urls import path
from . import views


urlpatterns = [
    path('', views.gallery, name='gallery'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('photo/<str:pk>/', views.view_photo, name='photo'),
    path('add/', views.add_photo, name='add'),
    path('delete/<int:pk>/', views.del_photo, name='del_photo')
]
