# Generated by Django 2.2.7 on 2020-02-19 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='age',
            field=models.CharField(default='', max_length=3, verbose_name='年齢'),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='sex',
            field=models.CharField(default='', max_length=3, verbose_name='性別'),
        ),
    ]
