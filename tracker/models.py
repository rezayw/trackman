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
    
    # Location details
    country = models.CharField(max_length=100, blank=True)
    country_code = models.CharField(max_length=10, blank=True)
    region = models.CharField(max_length=100, blank=True)
    region_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    timezone = models.CharField(max_length=100, blank=True)
    
    # Network details
    isp = models.CharField(max_length=200, blank=True)
    org = models.CharField(max_length=200, blank=True)
    as_number = models.CharField(max_length=200, blank=True)
    
    # Device details
    is_mobile = models.BooleanField(default=False)
    is_proxy = models.BooleanField(default=False)
    is_hosting = models.BooleanField(default=False)
    browser = models.CharField(max_length=100, blank=True)
    browser_version = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=100, blank=True)
    os_version = models.CharField(max_length=50, blank=True)
    device_type = models.CharField(max_length=50, blank=True)
    device_brand = models.CharField(max_length=100, blank=True)
    
    # Request details
    referrer = models.URLField(blank=True, null=True)
    accept_language = models.CharField(max_length=200, blank=True)
    
    time = models.DateTimeField(auto_now_add=True)
