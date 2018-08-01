from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone


class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    #content_type指向的是ContentType模型，这个模型是一个表，表中包含这个Django项目中的所有模型（全是小写），然后我们去选择它指向哪个模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()  #object_id是content_type指向模型的id
    content_object = GenericForeignKey('content_type', 'object_id') #通过上面的两项信息就可以获得到一个与content_type模型的具体对象

class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self) #获得ContentType指向的模型对象（ContentType表中的对象）
            readnum = ReadNum.objects.get(content_type=ct,object_id=self.pk)  #通过信息取得具体的模型（ct）对象，获得与这条模型对象关联的的具体的ReadNum对象
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
