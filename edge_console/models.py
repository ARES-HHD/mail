# encoding: utf-8

from django.db import models

class Preference(models.Model):

    key = models.CharField(max_length=128, db_index=True, unique=True)
    value = models.CharField(max_length=1024)
    desc = models.TextField("描述", blank=True)
    update_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = 'preference'

    def __unicode__(self):
        return u"%s: %s" % (self.key, self.value)