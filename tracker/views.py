
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io
from .models import TrackerLink, ClickLog
from .services import IPInfoService, UserAgentParser

def home(request):
    tracker_link = None

    if request.method == "POST":
        original_url = request.POST.get("original_url")
        if original_url:
            new_tracker = TrackerLink.objects.create(original_url=original_url)
            tracker_link = request.build_absolute_uri(f"/view/p/{new_tracker.uuid}/")

    return render(request, "tracker/home.html", {
        "tracker_link": tracker_link
    })

def dashboard(request):
    trackers = TrackerLink.objects.all().order_by('-created_at')
    return render(request, 'tracker/dashboard.html', {'trackers': trackers})

def detail(request, uuid):
    tracker = get_object_or_404(TrackerLink, uuid=uuid)
    clicks = tracker.clicks.all().order_by('-time')
    
    # Compute stats
    total = clicks.count()
    mobile = clicks.filter(is_mobile=True).count()
    stats = {
        'total': total,
        'mobile': mobile,
        'desktop': total - mobile,
        'proxy': clicks.filter(is_proxy=True).count(),
    }
    
    return render(request, 'tracker/detail.html', {
        'tracker': tracker,
        'clicks': clicks,
        'stats': stats,
    })

def download_pdf(request, uuid):
    tracker = get_object_or_404(TrackerLink, uuid=uuid)
    clicks = tracker.clicks.all().order_by('-time')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Colors
    primary_color = colors.HexColor('#e94560')
    dark_color = colors.HexColor('#1a1a2e')
    gray_color = colors.HexColor('#718096')
    
    def draw_header(page_num=1):
        # Header background
        p.setFillColor(dark_color)
        p.rect(0, height - 80, width, 80, fill=True, stroke=False)
        
        # Logo/Title
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 24)
        p.drawString(50, height - 50, "Trackman")
        
        # Subtitle
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.HexColor('#a0aec0'))
        p.drawString(50, height - 68, "Instagram Link Analytics Report")
        
        # Page number
        p.drawRightString(width - 50, height - 50, f"Page {page_num}")
    
    def draw_footer():
        p.setFillColor(gray_color)
        p.setFont("Helvetica", 8)
        p.drawString(50, 30, f"Generated on {tracker.created_at.strftime('%B %d, %Y at %H:%M')}")
        p.drawRightString(width - 50, 30, "Trackman - Instagram Link Tracker")
    
    # Page 1
    page_num = 1
    draw_header(page_num)
    
    # Report info section
    y = height - 120
    
    # Title
    p.setFillColor(dark_color)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Link Analytics Report")
    y -= 30
    
    # URL info box
    p.setFillColor(colors.HexColor('#f7fafc'))
    p.roundRect(50, y - 50, width - 100, 60, 8, fill=True, stroke=False)
    
    p.setFillColor(gray_color)
    p.setFont("Helvetica", 9)
    p.drawString(65, y - 10, "TRACKED URL")
    
    p.setFillColor(dark_color)
    p.setFont("Helvetica-Bold", 11)
    # Truncate URL if too long
    url_display = tracker.original_url[:70] + "..." if len(tracker.original_url) > 70 else tracker.original_url
    p.drawString(65, y - 28, url_display)
    
    p.setFillColor(gray_color)
    p.setFont("Helvetica", 9)
    p.drawString(65, y - 43, f"Created: {tracker.created_at.strftime('%B %d, %Y')}")
    
    y -= 80
    
    # Stats boxes
    total_clicks = clicks.count()
    mobile_clicks = clicks.filter(is_mobile=True).count()
    desktop_clicks = total_clicks - mobile_clicks
    proxy_clicks = clicks.filter(is_proxy=True).count()
    
    box_width = (width - 130) / 4
    stats = [
        ("Total Clicks", str(total_clicks), primary_color),
        ("Mobile", str(mobile_clicks), colors.HexColor('#4299e1')),
        ("Desktop", str(desktop_clicks), colors.HexColor('#48bb78')),
        ("VPN/Proxy", str(proxy_clicks), colors.HexColor('#ecc94b')),
    ]
    
    for i, (label, value, color) in enumerate(stats):
        x = 50 + i * (box_width + 10)
        
        # Box background
        p.setFillColor(color)
        p.roundRect(x, y - 55, box_width, 65, 6, fill=True, stroke=False)
        
        # Value
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(x + box_width/2, y - 25, value)
        
        # Label
        p.setFont("Helvetica", 9)
        p.drawCentredString(x + box_width/2, y - 45, label)
    
    y -= 90
    
    # Click details section
    p.setFillColor(dark_color)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Click Details")
    y -= 25
    
    # Table header
    p.setFillColor(dark_color)
    p.roundRect(50, y - 20, width - 100, 25, 4, fill=True, stroke=False)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 9)
    p.drawString(60, y - 13, "DATE & TIME")
    p.drawString(170, y - 13, "IP ADDRESS")
    p.drawString(280, y - 13, "LOCATION")
    p.drawString(420, y - 13, "DEVICE")
    p.drawString(490, y - 13, "VPN")
    
    y -= 30
    
    # Table rows
    p.setFont("Helvetica", 9)
    row_height = 35
    
    for i, click in enumerate(clicks):
        if y < 80:
            draw_footer()
            p.showPage()
            page_num += 1
            draw_header(page_num)
            y = height - 120
            
            # Redraw table header on new page
            p.setFillColor(dark_color)
            p.roundRect(50, y - 20, width - 100, 25, 4, fill=True, stroke=False)
            
            p.setFillColor(colors.white)
            p.setFont("Helvetica-Bold", 9)
            p.drawString(60, y - 13, "DATE & TIME")
            p.drawString(170, y - 13, "IP ADDRESS")
            p.drawString(280, y - 13, "LOCATION")
            p.drawString(420, y - 13, "DEVICE")
            p.drawString(490, y - 13, "VPN")
            
            y -= 30
            p.setFont("Helvetica", 9)
        
        # Alternating row background
        if i % 2 == 0:
            p.setFillColor(colors.HexColor('#f7fafc'))
            p.rect(50, y - row_height + 10, width - 100, row_height, fill=True, stroke=False)
        
        p.setFillColor(dark_color)
        
        # Date/Time
        p.drawString(60, y - 8, click.time.strftime("%b %d, %Y"))
        p.setFillColor(gray_color)
        p.setFont("Helvetica", 8)
        p.drawString(60, y - 20, click.time.strftime("%H:%M:%S"))
        p.setFont("Helvetica", 9)
        
        # IP
        p.setFillColor(dark_color)
        p.drawString(170, y - 13, click.ip[:18])
        
        # Location
        location = f"{click.city}, {click.country}" if click.city else click.country or "Unknown"
        p.drawString(280, y - 13, location[:20])
        
        # Device badge
        if click.is_mobile:
            p.setFillColor(colors.HexColor('#4299e1'))
            p.roundRect(420, y - 20, 50, 18, 3, fill=True, stroke=False)
            p.setFillColor(colors.white)
            p.setFont("Helvetica-Bold", 8)
            p.drawCentredString(445, y - 14, "Mobile")
        else:
            p.setFillColor(colors.HexColor('#48bb78'))
            p.roundRect(420, y - 20, 55, 18, 3, fill=True, stroke=False)
            p.setFillColor(colors.white)
            p.setFont("Helvetica-Bold", 8)
            p.drawCentredString(447, y - 14, "Desktop")
        
        # VPN badge
        p.setFont("Helvetica", 9)
        if click.is_proxy:
            p.setFillColor(colors.HexColor('#ecc94b'))
            p.roundRect(490, y - 20, 35, 18, 3, fill=True, stroke=False)
            p.setFillColor(dark_color)
            p.setFont("Helvetica-Bold", 8)
            p.drawCentredString(507, y - 14, "Yes")
        else:
            p.setFillColor(gray_color)
            p.setFont("Helvetica", 9)
            p.drawString(495, y - 13, "No")
        
        y -= row_height
    
    # Handle empty clicks
    if not clicks:
        p.setFillColor(gray_color)
        p.setFont("Helvetica-Oblique", 11)
        p.drawCentredString(width/2, y - 30, "No clicks recorded yet")
    
    draw_footer()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="trackman_report_{uuid}.pdf"'
    return response

def track_view(request, uuid):
    tracker = get_object_or_404(TrackerLink, uuid=uuid)
    
    # Get client IP (handle proxies)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    referrer = request.META.get('HTTP_REFERER', '')
    accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    
    # Get IP info
    ip_info = IPInfoService.get_ip_info(ip)
    
    # Parse user agent
    ua_info = UserAgentParser.parse(user_agent)
    
    ClickLog.objects.create(
        tracker=tracker,
        ip=ip,
        user_agent=user_agent,
        
        # Location
        country=ip_info.get('country', ''),
        country_code=ip_info.get('country_code', ''),
        region=ip_info.get('region', ''),
        region_name=ip_info.get('region_name', ''),
        city=ip_info.get('city', ''),
        zip_code=ip_info.get('zip_code', ''),
        lat=ip_info.get('lat'),
        lon=ip_info.get('lon'),
        timezone=ip_info.get('timezone', ''),
        
        # Network
        isp=ip_info.get('isp', ''),
        org=ip_info.get('org', ''),
        as_number=ip_info.get('as_number', ''),
        
        # Device
        is_mobile=ua_info.get('is_mobile', False),
        is_proxy=ip_info.get('proxy', False),
        is_hosting=ip_info.get('hosting', False),
        browser=ua_info.get('browser', ''),
        browser_version=ua_info.get('browser_version', ''),
        os=ua_info.get('os', ''),
        os_version=ua_info.get('os_version', ''),
        device_type=ua_info.get('device_type', ''),
        device_brand=ua_info.get('device_brand', ''),
        
        # Request
        referrer=referrer if referrer else None,
        accept_language=accept_language[:200] if accept_language else '',
    )

    return redirect(tracker.original_url)
