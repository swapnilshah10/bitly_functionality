from django.contrib import admin
from .models import Url,Ip , UniqueIp , FeatureToggle
# Register your models here.
admin.site.register(Url)
admin.site.register(Ip)
admin.site.register(UniqueIp)
admin.site.register(FeatureToggle)