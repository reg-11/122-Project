# Generated by Django 3.2.3 on 2021-05-24 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esko_app', '0004_auto_20210525_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
