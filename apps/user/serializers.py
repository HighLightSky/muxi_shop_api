from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.user.models import User
from utils.password_encode import get_md5


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        allow_blank=False, required=True,
        validators=[UniqueValidator(queryset=User.objects.all(),message="用户已经存在了")] # 验证器，验证唯一性
    )
    # password = serializers.CharField(write_only=True)  # 将pssword设置为只写，避免password被回传
    birthday = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    # 继承create()方法，create会被自动调用，这里可以做数据验证或者存储之前的数据加工
    def create(self, validated_data):
        # 这里做保存用户信息时的密码加密和保存数据操作
        validated_data["password"] = get_md5(validated_data["password"])
        validated_data["create_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = User.objects.create(**validated_data)
        return result

    class Meta:
        model = User
        fields = "__all__"


class UserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"