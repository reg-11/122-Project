# Generated by Django 3.2.3 on 2021-05-24 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esko_app', '0003_auto_20210524_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sns_account',
            field=models.URLField(blank=True),
        ),
    ]