from django.urls import path, re_path

from apps.order.views import OrderGoodsGenericAPIView, OrderGenericAPIView

urlpatterns = [
    path("", OrderGenericAPIView.as_view()),
    path('goods', OrderGoodsGenericAPIView.as_view()),
    # re_path('goods/(?P<trade_no>.*)', OrderGoodsGenericAPIView.as_view())
    path('goods/<trade_no>', OrderGoodsGenericAPIView.as_view())
]