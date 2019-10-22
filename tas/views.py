from django.http.response import JsonResponse
import oss2
from tas.models import TasSightsPic, TasSights
import demjson

access_id = ''
access_key = 'cbEtM63lQY6qYjpEocSOvkenySYLNz'


# 景点上传图片接口
def upload_file(request):
    """
        景点图片上传接口,通过阿里云oss jdk进行上传图片,并写入到数据库中
    """

    if request.method == 'POST':
        # 定义上传字段
        my_file = request.FILES.get('uploadfile', None)
        sid = request.POST.get('sid')
        bucket_key = request.POST.get('bucket_key', '')
        p_purpose = request.POST.get('p_purpose', None)
        p_copyright = request.POST.get('p_copyright', None)
        p_recommend = request.POST.get('p_recommend', None)
        hashcode = request.POST.get('hashcode', None)
        if not my_file:
            return JsonResponse({'status': 0, 'mes': '没有获取到图片,请检查上传方法'})
        else:
            try:
                # 阿里云AccessKey
                auth = oss2.Auth(access_id, access_key)
                # 外网地址 bucket名字
                bucket = oss2.Bucket(auth, 'oss-cn-shenzhen.aliyuncs.com', 'tas-saledb')
                # 通过bucket_key拼接上传路径,需要
                oss_file = bucket_key + my_file.name
                payload = bucket.put_object(oss_file, my_file)
                # 上传返回的url地址
                url = payload.resp.response.url
                # 写入数据库
                TasSightsPic.objects.create(sid=sid, bucket_key=bucket_key, p_purpose=p_purpose,
                                            p_copyright=p_copyright, p_recommend=p_recommend,
                                            hashcode=hashcode,
                                            savePath=url, pname=my_file.name)
            except oss2.exceptions.OssError as e:
                # 转换规则不正确的json格式为dict
                res = demjson.decode(str(e))
                return JsonResponse(res)
            except ValueError as e:
                return JsonResponse({'status': 0, 'mes': '数据库保存失败,请检查提交的字段属性是否正确'})
            else:
                return JsonResponse({'status': 1, 'mes': '上传成功'})


# 景点归类接口
def tas_sights(request):
    """
    根据old_id修改景点表,查询到就修改,没有则新增
    :param request:
    :return: 返回json
    """
    if request.method == 'POST':
        old_id = request.POST.get('old_id', None)
        city_id = request.POST.get('city_id', None)
        jdname = request.POST.get('jdname', None)
        jdename = request.POST.get('jdename', None)
        brief_en = request.POST.get('brief_en', None)
        brief_cn = request.POST.get('brief_cn', None)
        defaults = {
            'city_id': city_id,
            'jdname': jdname,
            'jdename': jdename,
            'brief_en': brief_en,
            'brief_cn': brief_cn
        }
        if None in (old_id, city_id):
            return JsonResponse({'status': 0, 'mes': '缺少old_id或city_id'})
        try:
            # 根据old_id修改或创建 返回一个元组 创建created返回True,修改created则返回False
            obj, created = TasSights.objects.update_or_create(old_id=old_id, defaults=defaults)
            print(obj.old_id)
        except ValueError as e:
            return JsonResponse({'status': 0, 'mes': str(e)})
        else:
            if created:
                return JsonResponse({'status': 1, 'mes': f'old_id:{obj.old_id}创建成功'})
            else:
                return JsonResponse({'status': 1, 'mes': f'old_id:{obj.old_id}修改成功'})
