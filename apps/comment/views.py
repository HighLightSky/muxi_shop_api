from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin

from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer
from utils import ResponseMessage
from utils.ResponseMessage import CommentResponse


# Create your views here.
class CommentGenericAPIView(ViewSetMixin,GenericAPIView,

                            CreateModelMixin,
                            ListModelMixin,
                            RetrieveModelMixin,
                            UpdateModelMixin,
                            DestroyModelMixin):
    queryset = Comment.objects
    serializer_class = CommentSerializer

    def single(self, request, pk):
        # 查询一条记录
        return self.retrieve(request, pk)

    def my_list(self, request):
        # 罗列所有记录
        return self.list(request)

    def edit(self, request, pk):
        # 更新记录
        return self.update(request, pk)

    def my_delete(self, request, pk):
        # 删除记录
        return self.destroy(request, pk)

    def my_save(self, request):
        # 保存记录
        return self.create(request)


class CommentAPIView(APIView):
    def get(self, request):
        sku_id = request.GET.get('sku_id')
        page = int(request.GET.get('page'))
        start = (page - 1) * 15
        end = page * 15

        db_result = Comment.objects.filter(sku_id=sku_id).all()[start:end]
        ser_data = CommentSerializer(db_result, many=True)

        return CommentResponse.success(ser_data.data)


class CommentCountAPIView(APIView):
    def get(self, request):
        sku_id = request.GET.get('sku_id')
        db_result = Comment.objects.filter(sku_id=sku_id).count()

        return CommentResponse.success(db_result)