# Generated by Django 3.2.3 on 2021-05-28 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esko_app', '0019_rename_name_comment_commenter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('sell', 'sell'), ('find', 'find'), ('services', 'services'), ('swap', 'swap')], max_length=8),
        ),
    ]
