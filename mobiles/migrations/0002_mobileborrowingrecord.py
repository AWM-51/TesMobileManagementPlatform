# Generated by Django 2.0.6 on 2019-04-03 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobileBorrowingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_id', models.IntegerField()),
                ('BorrowTime', models.TimeField()),
                ('ReturnTime', models.TimeField()),
                ('BorrowPeopleName', models.CharField(max_length=60)),
                ('ReturnPeopleName', models.CharField(max_length=60)),
            ],
        ),
    ]
