import decimal
import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from apps.goods.models import Goods, DecimalEncoder
from apps.goods.serializers import GoodsSerializer
from utils.ResponseMessage import GoodsResponse

# Create your views here.
# 获取商品信息的接口
class GoodsCategoryAPIView(APIView):
    def get(self, request, category_id, page):
        # 页面刷新时就判断用户登录是否还有效，如果过期，退出登录
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        current_page = (page - 1) * 20
        end_data = page * 20
        category_data = Goods.objects.filter(
            type_id=category_id
        ).all()[current_page:end_data]

        result_list = []
        for m in category_data:
            result_list.append(m.__str__())

        return GoodsResponse.success(result_list)


class GoodsDetailAPIView(APIView):
    def get(self, request, sku_id):
        # print(sku_id)
        goods_data = Goods.objects.filter(sku_id=sku_id).first()

        # 进行序列化动作 序列化参数instance 反序列化参数data
        result = GoodsSerializer(instance=goods_data)
        return GoodsResponse.success(result.data)


class GoodsFindAPIView(APIView):
    def get(self, request):
        goods_data = Goods.objects.filter(find=1).all()
        result = GoodsSerializer(instance=goods_data, many=True)
        return GoodsResponse.success(result.data)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")


# 使用原生SQL语句实现商品和评论关联查询
class GoodsSearchAPIView(APIView):
    def get(self, request, keyword, page, order_by):
        limit_page = (page - 1) * 15
        order_dict = {
            1: "r.comment_count",
            2: "g.p_price",

        }

        # 执行原生SQL
        from django.db import connection
        from muxi_shop_api import settings


        sql = """
        select r.comment_count, CONCAT('{}', g.image) as image, g.name, g.p_price, g.jd_price, g.shop_name, g.sku_id
        from goods g 
        left join 
        (
        select COUNT(c.sku_id) as comment_count, c.sku_id from comment c
        group by c.sku_id
        ) r 
        on g.sku_id = r.sku_id 
        where g.name like "%{}%" 
        order by {} desc limit {}, 30 
        """.format(settings.IMAGE_URL, keyword, order_dict[order_by], limit_page)

        cursor = connection.cursor()
        cursor.execute(sql)
        res = self.dict_fetchall(cursor)
        final_list = []
        for i in res:
            res_json = json.dumps(i, cls=DecimalEncoder, ensure_ascii=False)
            final_list.append(res_json)
        return GoodsResponse.success(final_list)


    def dict_fetchall(self, cursor):
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

class GoodsSearchDataCountAPIView(APIView):
    def get(self, request, keyword):
        count = Goods.objects.filter(name__contains=keyword).count()
        # print(count)
        return HttpResponse(count)