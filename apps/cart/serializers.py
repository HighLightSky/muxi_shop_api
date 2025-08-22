from rest_framework import serializers

from apps.cart.models import ShoppingCart
from apps.goods.models import Goods
from apps.goods.serializers import GoodsSerializer


class CartSerializer(serializers.ModelSerializer):
    sku_id = serializers.CharField(required=True)  # 设置验证规则，sku_id不能为空
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class CartDetailSerializer(serializers.Serializer):
    sku_id = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    nums = serializers.IntegerField()
    is_delete = serializers.IntegerField()
    # 关键：
    goods = serializers.SerializerMethodField()
    def get_goods(self, obj):
        # obj是实例化序列化器时传入的模型数据 ShoppingCart object (3)

        # 通过Goods的序列化器和模型实现关联查找数据
        ser = GoodsSerializer(Goods.objects.filter(sku_id=obj.sku_id).first()).data
        return ser


    # class Meta:
    #     model = ShoppingCart
    #     fields = '__all__'