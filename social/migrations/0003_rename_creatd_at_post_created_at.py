# Generated by Django 4.1.3 on 2022-11-09 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_alter_post_image_like_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='creatd_at',
            new_name='created_at',
        ),
    ]
