# Generated by Django 2.2.7 on 2019-11-28 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0008_auto_20191129_0416'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vote',
            options={'ordering': ['-date_created'], 'verbose_name': '投票', 'verbose_name_plural': '投票リスト'},
        ),
    ]