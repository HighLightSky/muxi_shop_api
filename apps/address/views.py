from django.db.models.expressions import result
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

from apps.address.models import UserAddress
from apps.address.serializers import AdressSerializer
from utils.jwt_auth import JwtQueryParamAuthentication, JwtHeaderAuthentication


# Create your views here.
class AddressGenericAPIView(GenericAPIView,
                            CreateModelMixin,
                            RetrieveModelMixin,
                            UpdateModelMixin,
                            DestroyModelMixin):
    queryset = UserAddress.objects.all()
    serializer_class = AdressSerializer
    authentication_classes = [JwtHeaderAuthentication, ]

    def post(self, request):
        return self.create(request)

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


class AddressListAPIView(GenericAPIView, ListModelMixin):
    queryset = UserAddress.objects
    serializer_class = AdressSerializer
    authentication_classes = [JwtQueryParamAuthentication, ]
    def get(self, request):
        # 拿到token验证返回的第一个值
        # print(request.user)  # {'status': True, 'data': {'username': 'sbsb@250.com', 'exp': 1754656584}, 'error': None}
        # 拿到token返回的第二个值
        # print(request.auth)  # token值
        # if not request.user["status"]:
        #     return
        return self.list(request)