from django.contrib.auth.models import ContentType
from .models import ReadNum

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" %  (ct.model,obj.pk)
    if not request.COOKIES.get(key):  # 检查浏览器中是否有一个cookie，有则代表该浏览器访问过页面，不再计数，没有则浏览器未访问，计数加1，并在后面的代码中向他发送一个cookie

        if ReadNum.objects.filter(content_type=ct ,object_id=obj.pk):  # 判断该类型下是否存在记录.count()
            readnum = ReadNum.objects.get(content_type=ct ,object_id=obj.pk)  # 存在记录，获得该记录
        else:
            readnum = ReadNum(content_type=ct ,object_id=obj.pk)  # 不存在记录,则创建一个记录并获得它
        readnum.read_num += 1
        readnum.save()
    return key