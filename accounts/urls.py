from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('upload-and-list/', views.upload_and_list_files, name='upload_and_list_files'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('visualize/<int:file_id>/', views.visualize, name='visualize'),
]
