from datetime import datetime

from django.db.models.expressions import result
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.order.models import OrderGoods, Order
from apps.user.models import User
from utils.password_encode import get_md5


class OrderGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

