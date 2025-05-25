import os
import io
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
from .models import TrackerLink, ClickLog

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_ip_info(ip):
    url = f"http://ip-api.com/json/{ip}?fields=66846719"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return {}

def home(request):
    if request.method == "POST":
        original_url = request.POST.get("original_url")
        if not original_url or not original_url.startswith(("http://", "https://")):
            return HttpResponseBadRequest("URL tidak valid")
        tracker, created = TrackerLink.objects.get_or_create(original_url=original_url)
        tracker_link = request.build_absolute_uri(f"/view/p/{tracker.uuid}")
        return render(request, "tracker/home.html", {"tracker_link": tracker_link})
    return render(request, "tracker/home.html")

def track_view(request, uuid):
    tracker = get_object_or_404(TrackerLink, uuid=uuid)

    ip = request.META.get("HTTP_X_FORWARDED_FOR")
    if ip:
        ip = ip.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "")

    ua = request.META.get("HTTP_USER_AGENT", "Unknown")
    info = get_ip_info(ip)

    ClickLog.objects.create(
        tracker=tracker,
        ip=ip,
        user_agent=ua,
        country=info.get("country", ""),
        region=info.get("regionName", ""),
        city=info.get("city", ""),
        zip_code=info.get("zip", ""),
        lat=info.get("lat", 0),
        lon=info.get("lon", 0),
        timezone=info.get("timezone", ""),
        isp=info.get("isp", ""),
        org=info.get("org", ""),
        as_info=info.get("as", ""),
        as_name=info.get("asname", ""),
        is_mobile=info.get("mobile", False),
        is_proxy=info.get("proxy", False),
    )

    return redirect(tracker.original_url)

def dashboard(request):
    trackers = TrackerLink.objects.all().order_by("-created_at")
    return render(request, "tracker/dashboard.html", {"trackers": trackers})

def detail(request, uuid):
    tracker = get_object_or_404(TrackerLink, uuid=uuid)
    clicks = tracker.clicks.all().order_by("-time")
    return render(request, "tracker/detail.html", {
        "tracker": tracker,
        "clicks": clicks,
        "google_maps_api_key": GOOGLE_MAPS_API_KEY,
    })

def download_pdf(request, uuid):
    tracker = get_object_or_404(TrackerLink, uuid=uuid)
    clicks = tracker.clicks.all().order_by("-time")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    y = 800
    p.setFont("Helvetica", 10)
    p.drawString(40, y, f"Tracker Report for {tracker.original_url}")
    y -= 30

    for click in clicks:
        if y < 50:
            p.showPage()
            y = 800
        proxy_str = "Pengguna menggunakan VPN" if click.is_proxy else "Tidak menggunakan VPN"
        mobile_str = "Pengguna menggunakan handphone" if click.is_mobile else "Bukan menggunakan handphone"
        line = f"{click.time} - IP: {click.ip} - {click.city}, {click.country} - {proxy_str} - {mobile_str}"
        p.drawString(40, y, line)
        y -= 20

    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")
