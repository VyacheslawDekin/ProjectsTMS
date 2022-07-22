import datetime

from django.db import models
from django.contrib.auth.models import User


class Posts(models.Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        ordering = ['created']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

        indexes = (
            models.Index(
                fields=['title', 'author']
            ),
        )

    def __str__(self):
        return f'{self.created} |  {self.title}'
