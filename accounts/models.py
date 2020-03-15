from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class UserInformation(models.Model):
    class Meta:
        verbose_name = 'ユーザー情報'
        verbose_name_plural = 'ユーザー情報'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='information')
    nickname = models.CharField(verbose_name='ニックネーム', max_length=20, null=True)
    sex = models.CharField(verbose_name='性別', max_length=3, null=True)
    age = models.IntegerField(verbose_name='年齢', null=True, validators=[MaxValueValidator(100), MinValueValidator(15)])
    secret = models.CharField(verbose_name='公開情報文字列', max_length=2, default='none')


class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='media/', null=True)
