
from django.urls import path

from .views import (
    PostListView,
    RegisterApi,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    SearchView,
    GetUserView,
    CreateView,
    AddCpuView,
    AddGpuView,
    AddRamView,
    OrderDetailView,
)

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('getuser/<pk>', GetUserView.as_view()),
    path('postlist/', PostListView.as_view()),
    path('post-create/', PostCreateView.as_view()),
    path('post-update/<pk>', PostUpdateView.as_view()),
    path('post-delete/<pk>', PostDeleteView.as_view()),
    path('search/', SearchView.as_view()),
    path('create/', CreateView.as_view()),
    path('add-cpu/', AddCpuView.as_view()),
    path('add-gpu/', AddGpuView.as_view()),
    path('add-ram/', AddRamView.as_view()),
    path('order/', OrderDetailView.as_view()),
]
