from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from apps.user.models import User
from apps.user.serializers import UserSerializer, UserBasicInfoSerializer
from utils import ResponseMessage
from utils.jwt_auth import create_token
from utils.password_encode import get_md5


# Create your views here.
class UserAPIView(APIView):
    # 已经可以实现功能，下面优化
    # def post(self, request):
    #     # MD5密码
    #     request.data["password"] = get_md5(request.data["password"])
    #     # 反序列化，将json变成对象
    #     user_data_serializer = UserSerializer(data=request.data)
    #     user_data_serializer.is_valid(raise_exception=True)
    #     user_data = User.objects.create(**user_data_serializer.data)
    #
    #     # 序列化一下 将json返回给前端
    #     user_ser = UserSerializer(instance=user_data)
    #     return JsonResponse(user_ser.data, safe=False)

    # 新增数据
    def post(self, request):
        # MD5密码
        request.data["password"] = get_md5(request.data["password"])
        # 反序列化，将json变成对象
        user_data_serializer = UserSerializer(data=request.data)
        user_data_serializer.is_valid(raise_exception=True)
        # user_data = User.objects.create(**user_data_serializer.data)
        user_data = user_data_serializer.save()
        # 这里调用了UserSerializer的create方法

        # 序列化一下 将json返回给前端
        user_ser = UserSerializer(instance=user_data)
        return ResponseMessage.UserResponse.success(user_ser.data)

    # 查询数据
    def get(self, request):
        email = request.GET.get("email")
        try:
            user_data = User.objects.get(email=email)
            user_ser = UserSerializer(instance=user_data)
            return ResponseMessage.UserResponse.success(user_ser.data)
        except Exception as e:
            print(e)
            return ResponseMessage.UserResponse.failed("用户信息获取失败")


class LoginView(GenericAPIView):
    def post(self, request):
        return_data = {}

        request_data = request.data
        email = request_data.get("username")
        user_data = User.objects.filter(email=email).first()
        if not user_data:
            return ResponseMessage.UserResponse.other("用户名错误")

        else:
            user_ser = UserSerializer(instance=user_data, many=False)
            # 用户输入的密码
            user_password_md5 = get_md5(request_data["password"])
            # 和数据库的密码比对
            if user_ser.data["password"] != user_password_md5:
                return ResponseMessage.UserResponse.other("密码错误")

            else:
                token_info = {
                    "username": email,
                }
                token_data = create_token(token_info)
                return_data["token"] = token_data
                return_data["username"] = user_ser.data["name"]
                return ResponseMessage.UserResponse.success(return_data)


class UserBasicInfoView(APIView):

    # 获取用户基本信息
    def get(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")
        user_data = User.objects.filter(email=email).first()
        user_ser = UserBasicInfoSerializer(instance=user_data)

        return ResponseMessage.UserResponse.success(user_ser.data)


    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        email = request.user.get("data").get("username")
        request_data = request.data
        name = request_data.get("name")
        gender = request_data.get("gender")
        birthday = request_data.get("birthday")

        User.objects.filter(email=email).update(name=name, gender=gender, birthday=birthday)

        user_updated = User.objects.filter(email=email).first()
        user_ser = UserSerializer(instance=user_updated)

        return ResponseMessage.UserResponse.success(user_ser.data)