
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import io
from .models import TrackerLink, ClickLog
from .services import IPInfoService

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
    return render(request, 'tracker/detail.html', {
        'tracker': tracker,
        'clicks': clicks
    })

def download_pdf(request, uuid):
    tracker = get_object_or_404(TrackerLink, uuid=uuid)
    clicks = tracker.clicks.all().order_by('-time')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(100, 800, f"Tracker Report for: {tracker.original_url}")
    y = 750
    for click in clicks:
        p.drawString(100, y, f"{click.time} - {click.ip} - {click.city}, {click.country}")
        y -= 20
        if y < 100:
            p.showPage()
            y = 800

    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="tracker_report_{uuid}.pdf"'
    return response

def track_view(request, uuid):
    tracker = get_object_or_404(TrackerLink, uuid=uuid)
    ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    ip_info = IPInfoService.get_ip_info(ip)
    is_mobile = 'mobile' in user_agent.lower()
    is_proxy = ip_info.get('proxy', False)

    ClickLog.objects.create(
        tracker=tracker,
        ip=ip,
        user_agent=user_agent,
        country=ip_info.get('country', ''),
        city=ip_info.get('city', ''),
        lat=ip_info.get('lat'),
        lon=ip_info.get('lon'),
        is_mobile=is_mobile,
        is_proxy=is_proxy
    )

    return redirect(tracker.original_url)
