from django.urls import path

from apps.goods.views import GoodsCategoryAPIView, GoodsDetailAPIView, GoodsFindAPIView, GoodsSearchAPIView, \
    GoodsSearchDataCountAPIView

urlpatterns = [
    path('category/<int:category_id>/<int:page>', GoodsCategoryAPIView.as_view(), name='category'),
    path('search/<str:keyword>/<int:page>/<int:order_by>', GoodsSearchAPIView.as_view(), name='search'),
    path('find', GoodsFindAPIView.as_view()),
    path('get_keyword_data_count/<str:keyword>', GoodsSearchDataCountAPIView.as_view()),
    path('<str:sku_id>', GoodsDetailAPIView.as_view(), name='detail'),
]