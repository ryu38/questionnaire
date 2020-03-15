# Generated by Django 2.2.7 on 2020-03-12 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_question_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='hide_name',
            field=models.BooleanField(default=False, verbose_name='匿名希望'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='choice',
            field=models.CharField(max_length=36, verbose_name='選択'),
        ),
    ]