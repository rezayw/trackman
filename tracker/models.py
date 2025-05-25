import uuid
from django.db import models

class TrackerLink(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid)

class ClickLog(models.Model):
    tracker = models.ForeignKey(TrackerLink, on_delete=models.CASCADE, related_name="clicks")
    ip = models.GenericIPAddressField()
    user_agent = models.TextField()
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    lat = models.FloatField()
    lon = models.FloatField()
    timezone = models.CharField(max_length=100)
    isp = models.CharField(max_length=255)
    org = models.CharField(max_length=255)
    as_info = models.CharField(max_length=255)
    as_name = models.CharField(max_length=255)
    is_mobile = models.BooleanField()
    is_proxy = models.BooleanField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip} - {self.city}, {self.country}"
