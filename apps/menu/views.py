import json

from django.db.models.expressions import result
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.menu.models import MainMenu, SubMenu
from utils.ResponseMessage import MenuResponse


# Create your views here.
class GoodsMainMenu(View):
    def get(self, request):
        main_menu = MainMenu.objects.all()
        result_list = []
        result_json = {}
        for m in main_menu:
            result_list.append(m.__str__()) # 必须显式调用
        # result_json['status'] = 1000
        # result_json['data'] = result_list
        # return HttpResponse(json.dumps(result_json), content_type='application/json')

        return MenuResponse.success(result_list)

    def post(self, request):
        pass


class GoodsSubMenu(View):
    def get(self, request):
        param_id = request.GET['main_menu_id']
        sub_menu = SubMenu.objects.filter(main_menu_id=param_id)
        result_list = []
        for m in sub_menu:
            result_list.append(m.__str__())

        # result_json['status'] = 1000
        # result_json['data'] = result_list
        # return HttpResponse(json.dumps(result_json), content_type='application/json', )
        return MenuResponse.success(result_list)