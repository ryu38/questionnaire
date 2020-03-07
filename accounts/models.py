from django.db import models
from django.contrib.auth.models import User


class UserInformation(models.Model):
    class Meta:
        verbose_name = 'ユーザー情報'
        verbose_name_plural = 'ユーザー情報'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sex = models.CharField(verbose_name='性別', max_length=3, null=True)
    age = models.CharField(verbose_name='年齢', max_length=3, null=True)
