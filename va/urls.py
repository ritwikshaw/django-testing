
from django.urls import path

from .views import (
    PostListView,
    RegisterApi,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    SearchView,
    GetUserView,
)

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('getuser/<pk>', GetUserView.as_view()),
    path('postlist/', PostListView.as_view()),
    path('post-create/', PostCreateView.as_view()),
    path('post-update/<pk>', PostUpdateView.as_view()),
    path('post-delete/<pk>', PostDeleteView.as_view()),
    path('search/', SearchView.as_view()),
]
