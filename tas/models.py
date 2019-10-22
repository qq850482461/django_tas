from django.db import models
from django.utils import timezone


class TasSightsPic(models.Model):
    """
    tas图片上传路径表
    """
    sid = models.IntegerField('sid', null=False)
    bucket_key = models.CharField('oss文件夹名称', max_length=250, null=False, default=None)
    pname = models.CharField('名字', max_length=250, null=True)
    p_purpose = models.IntegerField('景点用途，1封面，2内容', null=True)
    p_copyright = models.IntegerField('是否有版权', null=True)
    p_recommend = models.IntegerField('是否推荐', null=True)
    hashcode = models.CharField('哈希值', max_length=50, null=True)
    savePath = models.CharField('路径', max_length=250, null=True)
    uploadDate = models.DateTimeField('创建日期', default=timezone.now)

    class Meta:
        db_table = 'tas_sight_pic'

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<TAG:{0}>'.format(self.id)


class TasSights(models.Model):
    """
    tas景点信息更新表
    """
    old_id = models.IntegerField(null=False)
    jdname = models.CharField(max_length=250, null=True)
    jdename = models.CharField(max_length=250, null=True)
    city_id = models.IntegerField(null=False)
    brief_en = models.TextField(null=True)
    brief_cn = models.TextField(null=True)

    class Meta:
        db_table = 'tas_sights'

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<TAG:{0}>'.format(self.id)
