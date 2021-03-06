# Generated by Django 4.0.5 on 2022-07-02 19:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_posts_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='title',
            field=models.CharField(default=20220101, max_length=200),
            preserve_default=False,
        ),
    ]
