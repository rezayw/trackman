# Instagram Link Tracker (Django)

This project is a full-featured Instagram link tracker that:
- Shortens and tracks Instagram links
- Detects IP, city, country, proxy/VPN, and mobile device status
- Shows live location on a map using Leaflet + OpenStreetMap
- Exports click logs as PDF

---

## 🚀 Features
- Unique tracker link generation
- Click logging (IP, User-Agent, Location)
- Device & proxy detection
- Leaflet map rendering per click
- Admin dashboard
- PDF download
- Built with Django 5

---

## 🧱 Project Structure

```
instagram_tracker/
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    ├── asgi.py
tracker/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── services.py
    ├── admin.py
    └── templates/tracker/
static/
    └── tracker/css/, js/
```

---

## 🐳 Run with Docker

### 1. Build the container
```bash
docker build -t instagram-tracker .
```

### 2. Run the container
```bash
docker run -p 8180:8180 instagram-tracker
```

Visit:
```
http://localhost:8180
```

---

## ⚙️ Local Dev Setup

```bash
# Create venv and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create DB and run server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8180
```

---

## 📦 Dependencies

- Django
- python-dotenv
- requests
- reportlab
- leaflet.js (via CDN)

---
