# Generated by Django 2.0.6 on 2019-04-09 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobiles', '0010_auto_20190409_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='creatTime',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updateTime',
            field=models.TimeField(auto_now=True),
        ),
    ]
