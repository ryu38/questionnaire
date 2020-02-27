from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    class Meta:
        verbose_name = '質問'
        verbose_name_plural = '質問リスト'
        ordering = ['-date_created']

    text = models.TextField(verbose_name='質問', max_length=255, null=True)
    date_created = models.DateTimeField(verbose_name='投稿日時', default=timezone.now)
    like_num = models.IntegerField(verbose_name='いいね！', default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_create_user', null=True)
    expired = models.BooleanField(verbose_name='締め切り', default=False)

    def __str__(self):
        return self.text


class Choice(models.Model):
    class Meta:
        verbose_name = '選択'
        verbose_name_plural = '選択リスト'

    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice = models.CharField(verbose_name='選択', max_length=50)
    vote_num = models.IntegerField(verbose_name='投票数', default=0)

    def __str__(self):
        return self.choice


class Like(models.Model):
    class Meta:
        verbose_name = 'いいね！'
        verbose_name_plural = 'いいね！リスト'
        ordering = ['-date_created']

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)


class Vote(models.Model):
    class Meta:
        verbose_name = '投票'
        verbose_name_plural = '投票リスト'
        ordering = ['-date_created']

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote_user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes', null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
