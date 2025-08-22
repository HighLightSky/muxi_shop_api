import json

from django.http import HttpResponse, JsonResponse


# 菜单状态，1 开头
class MenuResponse:
    @staticmethod
    def success(data):
        return HttpResponse(json.dumps({'status': 1000, 'data': data}), content_type='application/json')

    @staticmethod
    def failed(data):
        return HttpResponse(json.dumps({'status': 1001, 'data': data}), content_type='application/json')

    @staticmethod
    def other(data):
        return HttpResponse(json.dumps({'status': 1002, 'data': data}), content_type='application/json')

# 商品状态，2 开头
class GoodsResponse:
    @staticmethod
    def success(data):
        return HttpResponse(json.dumps({'status': 2000, 'data': data}), content_type='application/json')

    @staticmethod
    def failed(data):
        return HttpResponse(json.dumps({'status': 2001, 'data': data}), content_type='application/json')

    @staticmethod
    def other(data):
        return HttpResponse(json.dumps({'status': 2002, 'data': data}), content_type='application/json')

# 购物车状态，3 开头
class CartResponse:
    @staticmethod
    def success(data):
        result = {'status': 3000, 'data': data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def failed(data):
        result = {'status': 3001, 'data': data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def other(data):
        result = {'status': 3002, 'data': data}
        return JsonResponse(result, safe=False)


# 用户状态，4 开头
class UserResponse:
    @staticmethod
    def success(data):
        result = {'status': 4000, 'data': data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def failed(data):
        result = {'status': 4001, 'data': data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def other(data):
        result = {'status': 4002, 'data': data}
        return JsonResponse(result, safe=False)

# 评论状态，5 开头
class CommentResponse:
    @staticmethod
    def success(data):
        result = {'status': 5000, 'data': data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def failed(data):
        result = {'status': 5001, 'data': data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def other(data):
        result = {'status': 5002, 'data': data}
        return JsonResponse(result, safe=False)


# 订单状态，6 开头
class OrderResponse:
    @staticmethod
    def success(data):
        result = {'status': 6000, 'data': data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def failed(data):
        result = {'status': 6001, 'data': data}
        return JsonResponse(result, safe=False)

    @staticmethod
    def other(data):
        result = {'status': 6002, 'data': data}
        return JsonResponse(result, safe=False)