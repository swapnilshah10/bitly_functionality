from django.db import models
from django.utils import timezone
import string
import random


class Url(models.Model):
    long_url = models.URLField(max_length=2000)
    short_url = models.CharField(max_length=20, unique=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    ip = models.CharField(max_length=100 , blank = True , default = "")
    ip2 = models.ForeignKey('UniqueIp', on_delete=models.CASCADE , blank = True , null = True)
    name = models.CharField(max_length=200, unique=False , null = True)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = create_short_url()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.long_url

    def get_absolute_url(self):
        return self.long_url

class Ip(models.Model):
    ip = models.CharField(max_length=100 , blank = True , default = "")
    latitude = models.CharField(max_length=100 , blank = True , default = "")
    longitude  = models.CharField(max_length=100 , blank = True , default = "")
    method  = models.CharField(max_length=100 , blank = True , default = "")
    page  = models.CharField(max_length=100 , blank = True , default = "")
    city = models.CharField(max_length=100 , blank = True , default = "")
    time = models.DateTimeField(default=timezone.now , blank = True)
    def __str__(self):
        return self.ip +" " +self.page + " |  " + self.time.strftime("%Y-%m-%d %H:%M:%S")

def create_short_url():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    short_id = ''.join(random.choices(chars, k=6))
    while Url.objects.filter(short_url=short_id).exists():
      short_id = ''.join(random.choices(chars, k=6))
    return short_id

class UniqueIp(models.Model):
    ip = models.CharField(max_length=100 , default = "" , unique = True)
    def __str__(self):
        return self.ip


class FeatureToggle(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}: {'Enabled' if self.is_enabled else 'Disabled'}"