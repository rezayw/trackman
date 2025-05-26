import requests
from django.conf import settings

class IPInfoService:
    @staticmethod
    def get_ip_info(ip):
        if not ip or ip == '127.0.0.1':
            return {}
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", params={'fields': '66846719'}, timeout=3)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return {}
