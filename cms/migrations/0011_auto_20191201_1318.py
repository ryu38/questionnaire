# Generated by Django 2.2.7 on 2019-12-01 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_auto_20191130_0255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='text',
            new_name='question',
        ),
    ]