# Generated by Django 3.0.4 on 2020-06-09 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_profile', '0004_auto_20200609_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilefile',
            name='file',
            field=models.FileField(upload_to='files'),
        ),
    ]