# Generated by Django 2.2.3 on 2020-07-23 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_smart_redis', '0002_smartcache_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='smartcache',
            name='qs',
            field=models.TextField(default='', verbose_name='Query String'),
            preserve_default=False,
        ),
    ]