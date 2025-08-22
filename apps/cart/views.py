
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.context_processors import request
from rest_framework.views import APIView

from apps.cart.models import ShoppingCart
from apps.cart.serializers import CartSerializer, CartDetailSerializer
from utils import ResponseMessage


# Create your views here.
class CartAPIView(APIView):
    # @todo 登陆后才能访问的功能实现

    def post(self, request):
        request_data = request.data
        # email = request_data.get('email') # 也可以写request_data["email"] 但是如果不存在则会报错
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        # 从token中获取email
        email = request.user.get("data").get("username")
        request_data["email"] = email
        sku_id = request_data.get('sku_id')
        nums = request_data.get('nums')
        is_delete = request_data.get('is_delete')

        # 判断数据是否存在 不存在则创建 存在则更新
        data_exists = ShoppingCart.objects.filter(email=email,
                                    sku_id=sku_id,
                                    is_delete=0)
        # 存在就更新
        if data_exists.exists():
            exist_cart_data = data_exists.get(email=email,
                            sku_id=sku_id,
                            is_delete=0)

            if is_delete == 0:
                new_nums = nums + exist_cart_data.nums
                request_data['nums'] = new_nums

            elif is_delete == 1:
                request_data['nums'] = exist_cart_data.nums

                # 反序列化
            cart_ser = CartSerializer(data=request_data)
            cart_ser.is_valid(raise_exception=True)
            ShoppingCart.objects.filter(email=email,
                                        sku_id=sku_id,
                                        is_delete=0).update(**cart_ser.data) # 先查询到数据再更新
            return ResponseMessage.CartResponse.success("更新成功")

        # 不存在就插入
        else:
            cart_ser = CartSerializer(data=request_data)  # 序列化
            cart_ser.is_valid(raise_exception=True)  # 必须要验证数据，验证规则在serializers.py
            ShoppingCart.objects.create(**cart_ser.data)
            return ResponseMessage.CartResponse.success("插入成功")


    def get(self, request):
        # 判断登录
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.GET.get('email')
        cart_result = ShoppingCart.objects.filter(email=email, is_delete=0)
        cart_ser = CartSerializer(instance=cart_result, many=True)  # 序列化器默认只有一条数据传入，这里告诉她传入多条
        return ResponseMessage.CartResponse.success(cart_ser.data)


# 使用序列化器实现多表关联查询
class CartDetailAPIView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        # 查询条件
        filters = {
            "email": request.user.get("data").get("username"),
            "is_delete": 0
        }
        shopping_cart = ShoppingCart.objects.filter(**filters).all()
        db_data = CartDetailSerializer(shopping_cart, many=True)

        return ResponseMessage.CartResponse.success(db_data.data)


class UpdateCartNumAPIView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        # 从token中获取email
        # request.user:{'status': True, 'data': {'username': '4@qq.com', 'exp': 1815617711}, 'error': None}
        email = request.user.get("data").get("username")
        request_data = request.data
        ShoppingCart.objects.filter(email=email,
                                    sku_id=request_data["sku_id"],
                                    is_delete=0).update(nums=request_data["nums"])
        return ResponseMessage.CartResponse.success("ok")


# 获取购物车商品数量的接口
class CartCountAPIView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")
        user_cart_count = ShoppingCart.objects.filter(email=email,
                                    is_delete=0).count()
        print(user_cart_count)

        return ResponseMessage.CartResponse.success(user_cart_count)


class DeleteCartGoodsAPIView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        # 从token中获取email
        # request.user:{'status': True, 'data': {'username': '4@qq.com', 'exp': 1815617711}, 'error': None}
        email = request.user.get("data").get("username")
        request_data = request.data
        ShoppingCart.objects.filter(email=email,
                                    sku_id__in=request_data,
                                    is_delete=0).update(is_delete=1)
        return ResponseMessage.CartResponse.success("ok")