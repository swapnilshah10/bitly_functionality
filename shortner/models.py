from django.db import models
from django.utils import timezone
import string
import random
from django.db import models


class Url(models.Model):
    long_url = models.URLField(max_length=2000)
    short_url = models.CharField(max_length=20, unique=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = create_short_url()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.long_url

    def get_absolute_url(self):
        return self.long_url


def create_short_url():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    short_id = ''.join(random.choices(chars, k=6))
    return short_id
