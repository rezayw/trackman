import uuid
from django.db import models

class TrackerLink(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_url

class ClickLog(models.Model):
    tracker = models.ForeignKey(TrackerLink, on_delete=models.CASCADE, related_name='clicks')
    ip = models.CharField(max_length=100)
    user_agent = models.TextField()
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    is_mobile = models.BooleanField(default=False)
    is_proxy = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
