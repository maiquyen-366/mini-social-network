"""Tầng route posts: ánh xạ endpoint bài, comment và like."""

from django.urls import path

from posts.controllers import CommentListCreateController, LikeToggleController, PostDetailController, PostListCreateController

urlpatterns = [
    path("", PostListCreateController.as_view()),
    path("<int:post_id>/", PostDetailController.as_view()),
    path("<int:post_id>/like/", LikeToggleController.as_view()),
    path("<int:post_id>/comments/", CommentListCreateController.as_view()),
]
