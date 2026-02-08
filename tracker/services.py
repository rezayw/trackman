import requests
import re
from django.conf import settings

class IPInfoService:
    @staticmethod
    def get_ip_info(ip):
        if not ip or ip in ('127.0.0.1', 'localhost', '::1'):
            return {'is_local': True}
        try:
            # Use ip-api.com with all fields
            response = requests.get(
                f"http://ip-api.com/json/{ip}",
                params={'fields': 'status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,proxy,hosting,query'},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', ''),
                    'country_code': data.get('countryCode', ''),
                    'region': data.get('region', ''),
                    'region_name': data.get('regionName', ''),
                    'city': data.get('city', ''),
                    'zip_code': data.get('zip', ''),
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'timezone': data.get('timezone', ''),
                    'isp': data.get('isp', ''),
                    'org': data.get('org', ''),
                    'as_number': data.get('as', ''),
                    'proxy': data.get('proxy', False),
                    'hosting': data.get('hosting', False),
                }
            return {}
        except requests.RequestException:
            return {}


class UserAgentParser:
    """Parse user agent string to extract browser, OS, and device info"""
    
    BROWSERS = [
        (r'Firefox/(\d+\.?\d*)', 'Firefox'),
        (r'Edg/(\d+\.?\d*)', 'Edge'),
        (r'OPR/(\d+\.?\d*)', 'Opera'),
        (r'Chrome/(\d+\.?\d*)', 'Chrome'),
        (r'Safari/(\d+\.?\d*)', 'Safari'),
        (r'MSIE\s(\d+\.?\d*)', 'Internet Explorer'),
        (r'Trident.*rv:(\d+\.?\d*)', 'Internet Explorer'),
    ]
    
    OPERATING_SYSTEMS = [
        (r'Windows NT 10\.0', 'Windows', '10/11'),
        (r'Windows NT 6\.3', 'Windows', '8.1'),
        (r'Windows NT 6\.2', 'Windows', '8'),
        (r'Windows NT 6\.1', 'Windows', '7'),
        (r'Mac OS X (\d+[._]\d+)', 'macOS', None),
        (r'Android (\d+\.?\d*)', 'Android', None),
        (r'iPhone OS (\d+[._]\d+)', 'iOS', None),
        (r'iPad.*OS (\d+[._]\d+)', 'iPadOS', None),
        (r'Linux', 'Linux', ''),
        (r'Ubuntu', 'Ubuntu', ''),
        (r'CrOS', 'Chrome OS', ''),
    ]
    
    DEVICES = [
        (r'iPhone', 'Mobile', 'Apple'),
        (r'iPad', 'Tablet', 'Apple'),
        (r'Android.*Mobile', 'Mobile', 'Android'),
        (r'Android.*Tablet|Android(?!.*Mobile)', 'Tablet', 'Android'),
        (r'Samsung', 'Mobile', 'Samsung'),
        (r'Pixel', 'Mobile', 'Google'),
        (r'Macintosh', 'Desktop', 'Apple'),
        (r'Windows', 'Desktop', 'PC'),
    ]
    
    @classmethod
    def parse(cls, user_agent):
        if not user_agent:
            return {}
        
        result = {
            'browser': '',
            'browser_version': '',
            'os': '',
            'os_version': '',
            'device_type': 'Desktop',
            'device_brand': '',
            'is_mobile': False,
        }
        
        # Parse browser
        for pattern, name in cls.BROWSERS:
            match = re.search(pattern, user_agent, re.IGNORECASE)
            if match:
                result['browser'] = name
                result['browser_version'] = match.group(1) if match.lastindex else ''
                break
        
        # Parse OS
        for pattern, name, version in cls.OPERATING_SYSTEMS:
            match = re.search(pattern, user_agent, re.IGNORECASE)
            if match:
                result['os'] = name
                if version:
                    result['os_version'] = version
                elif match.lastindex:
                    result['os_version'] = match.group(1).replace('_', '.')
                break
        
        # Parse device
        for pattern, device_type, brand in cls.DEVICES:
            if re.search(pattern, user_agent, re.IGNORECASE):
                result['device_type'] = device_type
                result['device_brand'] = brand
                break
        
        # Check if mobile
        mobile_keywords = ['Mobile', 'Android', 'iPhone', 'iPad', 'iPod', 'webOS', 'BlackBerry', 'Opera Mini', 'IEMobile']
        result['is_mobile'] = any(kw.lower() in user_agent.lower() for kw in mobile_keywords)
        
        return result
