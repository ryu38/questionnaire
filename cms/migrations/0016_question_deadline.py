# Generated by Django 2.2.7 on 2020-03-05 07:15

import cms.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0015_delete_userinformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='deadline',
            field=models.DateTimeField(default=cms.models.tomorrow, null=True, verbose_name='締め切り'),
        ),
    ]
