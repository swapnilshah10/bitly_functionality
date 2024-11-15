from .models import Url
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Url
        fields = ['long_url', 'short_url', 'clicks', 'created_at']

