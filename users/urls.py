from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.users_list, name='users_list'),
    path('create/', views.user_create, name='user_create'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
    path('update/<int:pk>/', views.user_update, name='user_update'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),
]
