import time
from tkinter.constants import SEL_FIRST

from django.contrib.admin.utils import lookup_field
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.generics import GenericAPIView

from apps.cart.models import ShoppingCart
from apps.order.models import OrderGoods, Order
from apps.order.serializers import OrderGoodsSerializer, OrderSerializer
from utils.ResponseMessage import OrderResponse


# 这里继承GenericAPIView，把序列化器和数据模型单独拿出来，便于后期维护
# queryset是对应的数据模型  serializer_class是对应的序列化器
class OrderGoodsGenericAPIView(GenericAPIView):
    queryset = OrderGoods.objects
    serializer_class = OrderGoodsSerializer

    # 使用什么字段进行查询，默认pk
    lookup_field = 'trade_no'

    def post(self, request):
        serializer = self.get_serializer
        queryset = self.get_queryset


        order_goods_data_ser = serializer(data=request.data)
        order_goods_data_ser.is_valid(raise_exception=True)
        order_goods_data_ser.save()
        return HttpResponse("post输出")

    def get(self, request, trade_no):
        # get_object()通过配置的lookup_field = 'trade_no'查询,对象不存在时自动返回 404 Not Found
        # get_queryset()返回queryset变量的查询结果，这里会返回数据表中所有数据

        # @todo 这里不知道返回的数据有一条还是多条，many属性设置需要动态变化
        ser = self.get_serializer(instance=self.get_object(), many=False)
        # ser = self.get_serializer(instance=self.get_queryset(), many=True)
        return JsonResponse(ser.data, safe=False)


class OrderGenericAPIView(GenericAPIView):
    queryset = Order.objects
    serializer_class = OrderSerializer

    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")
        # 生成订单号
        trade_no = int(time.time()*1000)
        request_data = request.data
        trade_data = request_data["trade"]  # 订单数据
        goods_data = request_data["goods"]  # 商品数据
        trade_data["trade_no"] = trade_no
        trade_data["email"] = email
        # 新创建的订单状态0
        trade_data["pay_status"] = 0
        serializer = self.get_serializer(data=trade_data)
        serializer.is_valid(raise_exception=True)
        # 保存订单数据
        serializer.save()

        goods_order_data = {}

        # 处理订单中的商品
        for data in goods_data:

            goods_order_data["trade_no"] = trade_no
            goods_order_data["sku_id"] = data["sku_id"]
            goods_order_data["goods_num"] = data["nums"]
            OrderGoods.objects.create(**goods_order_data)

            ShoppingCart.objects.filter(
                sku_id=data["sku_id"],
                email=trade_data["email"]
            ).update(is_delete=1)

        return OrderResponse.success(serializer.data)