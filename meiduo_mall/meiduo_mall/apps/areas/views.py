from django.shortcuts import render
from django.views import View
from django import http
import logging
from django.core.cache import cache

from .models import Area
from utils.response_code import RETCODE
# Create your views here.

logger = logging.getLogger('django')

"""省市区三级联动"""
class AreaView(View):
    def get(self, request):
        # 先要判断是要查询省级数据还是市区级数据
        area_id = request.GET.get('area_id')
        if not area_id:
            # 尝试进行读取缓存数据
            province_list = cache.get('province_list')
            if not province_list:
                try:
                    # 查询省级             Area.objects.filter(属性名__条件表达式=值)
                    province_model_list = Area.objects.filter(parent__isnull=True)
                    # 将模型列表转成字典列表
                    province_list = []
                    for province_model in province_model_list:
                        province_dict ={'id': province_model.id,'name': province_model.name,}
                        province_list.append(province_dict)
                    # 进行省级字典数据的缓存(默认存储到别名为"default"的配置中，即0号库)
                    cache.set('province_list',province_list,3600)
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code':RETCODE.DBERR, 'errmsg':'查询省份数据错误'})
            # 返回json数据(格式大概就是这样)
            """
            {
                "code": "0",
                "errmsg": "ok",
                "province_list": [
                    {
                        "id": 110000,
                        "name": "北京市"
                    },
                    .....。。。。
                ]
            }
            """
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'province_list': province_list})  # code='0'
        else:
            # 先进性缓存读取
            sub_data = cache.get('sub_area_' + area_id)
            if not sub_data:
                try:
                    # 查询市区级(运行在这里，说明有area_id数据)
                    # 通过id进行查找
                    parent_model = Area.objects.get(id=area_id)
                    # 现在要通过父级来进行查找，是一查多的类型
                             #默认为: parent_model.area_set.all()，但在设计Area模型时，自定义了related_name='subs'
                    sub_model_list = parent_model.subs.all()
                    # 现在进行构造前端的json的数据
                    subs = []
                    for sub_model in sub_model_list:
                        sub_dict ={'id': sub_model.id,'name': sub_model.name,}
                        subs.append(sub_dict)
                    # 主要要返回的数据
                    sub_data = {
                        'id': parent_model.id,
                        'name': parent_model.name,
                        'subs':subs
                    }
                    # 进行存储市级或区县级数据
                    cache.set('sub_area_' + area_id,sub_data,3600)
                    # 响应城市或区县JSON数据:大致如下
                    """
                    "code": "0",
                    "errmsg": "OK",
                    "sub_data":{
                            "id":1300000,
                            "name":"河北省",
                            "subs":[
                                    "id":130100,
                                    "name":"石家庄市"
                                    ]
                            }
                    """
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '查询市级或区县级数据错误'})
            # 返回json数据
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'sub_data': sub_data})
