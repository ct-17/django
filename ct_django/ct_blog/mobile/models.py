from django.db import models
from django.conf import settings

class MobileModel(models.Model):
    objects = models.Manager()
    title           = models.CharField(max_length=255, blank=True)
    image           = models.ImageField(upload_to='mobile/')
    contend         = models.TextField()
    upload_time     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
