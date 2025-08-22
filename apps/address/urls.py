from django.urls import path

from apps.address.views import AddressGenericAPIView, AddressListAPIView

urlpatterns = [
    path('', AddressGenericAPIView.as_view()),
    path('list', AddressListAPIView.as_view()),
    path('<pk>', AddressGenericAPIView.as_view()),

]