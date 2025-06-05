
from django.urls import path
from .views import *

urlpatterns = [
    path("register/",UserRegistrationView.as_view()),
    path("login/",LoginView.as_view()),
    path("user/",UserDetailView.as_view()),
    
    # path("posts/", BlogPostListCreateView.as_view()),
    # path("posts/<int:pk>/", BlogPostRetrieveUpdateDeleteView.as_view()),

    # path("comments/", CommentCreateView.as_view()),
    # path("posts/<int:post_id>/comments/", PostCommentsListView.as_view()),

    # path("posts/<int:post_id>/like/", LikeCreateView.as_view()),
    # path("posts/<int:post_id>/likes/", PostLikesListView.as_view()),
]