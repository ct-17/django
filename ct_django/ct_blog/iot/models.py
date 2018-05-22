from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    objects         = models.Manager()
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='author1')
    title           = models.CharField(max_length=255, blank=True)
    img             = models.ImageField(upload_to='iot/')
    contend         = models.TextField()
    upload_time     = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.upload_time = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='author_iot')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    