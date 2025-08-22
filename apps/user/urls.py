from django.urls import path

from apps.user.views import UserAPIView, LoginView, UserBasicInfoView

urlpatterns = [
    path('', UserAPIView.as_view()),
    path('login', LoginView.as_view()),
    path('basic_info', UserBasicInfoView.as_view())
]