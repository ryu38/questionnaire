# Generated by Django 2.2.7 on 2019-11-28 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0007_auto_20191129_0145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='vote',
            new_name='vote_num',
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Choice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '投票',
                'verbose_name_plural': 'いいね！リスト',
                'ordering': ['-date_created'],
            },
        ),
    ]
