import requests
from django.conf import settings

class IPInfoService:
    @staticmethod
    def get_ip_info(ip):
        if not ip or ip == '127.0.0.1':
            return {}
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
            response.raise_for_status()
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', ''),
                    'city': data.get('city', ''),
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'proxy': data.get('proxy', False),
                }
            return {}
        except requests.RequestException:
            return {}
