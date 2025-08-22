from django.urls import path

from apps.comment.views import CommentGenericAPIView, CommentAPIView, CommentCountAPIView

urlpatterns = [
    path('', CommentGenericAPIView.as_view({
        "get": "my_list",
        "post": "my_save"
    })),
    path('detail', CommentAPIView.as_view()),
    path('count', CommentCountAPIView.as_view()),
    path('<pk>', CommentGenericAPIView.as_view({
        "get": "single",
        "post": "edit",
        "delete": "my_delete"
    })),
]