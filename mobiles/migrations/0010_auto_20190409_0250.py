# Generated by Django 2.0.6 on 2019-04-09 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobiles', '0009_auto_20190409_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='u_token',
            field=models.CharField(default='', max_length=100),
        ),
    ]
