# 创建一个序列化器，自动实现序列化
from rest_framework import serializers

from apps.goods.models import Goods
from muxi_shop_api.settings import IMAGE_URL


class GoodsSerializer(serializers.ModelSerializer):
    # 这里面写的字段就是想序列化处理的字段
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        new_image_path = IMAGE_URL + obj.image
        return new_image_path

    class Meta:
        model = Goods
        fields = '__all__'