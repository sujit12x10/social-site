from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_comment_create_and_list_view, name='main-post-view'),
    path('liked/', views.like_unlike_post, name='post-like-view'),
    path('<pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('<pk>/delete/', views.PostdeleteView.as_view(), name='post-delete'),

    # path('test/', views.test_view)
]