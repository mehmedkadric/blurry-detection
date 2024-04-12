from django.db import models


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    threshold = models.IntegerField(default=100)
    is_blurry = models.BooleanField(default=False)
    bluriness_level = models.FloatField(default=0)
