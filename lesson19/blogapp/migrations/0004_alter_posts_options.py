# Generated by Django 4.0.5 on 2022-07-02 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_posts_created_posts_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ['created'], 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
    ]
