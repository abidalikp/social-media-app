# Generated by Django 4.1.3 on 2022-11-14 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_like_isliked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='isLiked',
        ),
    ]
