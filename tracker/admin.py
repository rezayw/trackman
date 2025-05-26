from django.contrib import admin
from .models import TrackerLink, ClickLog

@admin.register(TrackerLink)
class TrackerLinkAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'uuid', 'created_at')
    search_fields = ('original_url', 'uuid')
    readonly_fields = ('uuid', 'created_at')

@admin.register(ClickLog)
class ClickLogAdmin(admin.ModelAdmin):
    list_display = ('tracker', 'ip', 'country', 'city', 'time')
    list_filter = ('country', 'is_mobile', 'is_proxy')
    search_fields = ('ip', 'city', 'country')
    readonly_fields = ('time',)