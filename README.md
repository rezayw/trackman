# Trackman

<p align="center">
  <img src="https://blogger.googleusercontent.com/img/a/AVvXsEjj_TUmaZgc5jEKRJ0Awnjrvv048L8FpXo8nzz0zrAnz05aJpu3YAZjZGDJqLhWTD4l5gPG-9baigCUzHXnN85_O32613Sb5u9udzrO9s5C4TgIl0Zw9dLPXuCzojP1H5VHuhP5NTNaRLqhvczI54-o5kCSkP6hz0HuqPAhLjRZfs0_xyvbSIz35UbgrlZG" alt="Trackman Screenshot" width="800">
</p>

<p align="center">
  <strong>A powerful Instagram link tracker with detailed analytics</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#demo">Demo</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#api">API</a>
</p>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔗 **Link Shortening** | Generate unique trackable URLs for any Instagram link |
| 📍 **Location Tracking** | IP geolocation with country, region, city, ZIP, and coordinates |
| 🌐 **Network Analysis** | ISP, organization, AS number detection |
| 🛡️ **VPN/Proxy Detection** | Identify visitors using VPNs, proxies, or datacenter IPs |
| 📱 **Device Detection** | Browser, OS, device type, and brand identification |
| 🗺️ **Interactive Maps** | Live location rendering with Leaflet + OpenStreetMap |
| 📊 **Analytics Dashboard** | Real-time click statistics and visitor insights |
| 📄 **PDF Reports** | Export detailed click logs as professional PDF reports |
| 🌙 **Dark Mode UI** | Modern, responsive dark theme interface |

---

## 🛠️ Tech Stack

- **Backend:** Django 6.x (Python 3.11+)
- **Frontend:** HTML5, CSS3, JavaScript
- **Maps:** Leaflet.js + OpenStreetMap
- **PDF Generation:** ReportLab
- **IP Geolocation:** ip-api.com
- **Icons:** Font Awesome 6

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- pip

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/trackman.git
cd trackman

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver 8180
```

Visit: **http://localhost:8180**

### 🐳 Docker

```bash
# Build the image
docker build -t trackman .

# Run the container
docker run -p 8180:8180 trackman
```

---

## 🚀 Usage

1. **Create a Tracker** - Paste an Instagram URL on the home page
2. **Share the Link** - Copy the generated tracker URL and share it
3. **Monitor Clicks** - View real-time analytics on the dashboard
4. **Export Reports** - Download PDF reports for each tracker

---

## 📁 Project Structure

```
trackman/
├── instagram_tracker/      # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tracker/                # Main application
│   ├── models.py          # TrackerLink, ClickLog models
│   ├── views.py           # View controllers
│   ├── services.py        # IP lookup & UA parsing
│   └── urls.py            # URL routing
├── templates/tracker/      # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   └── detail.html
├── static/tracker/         # Static assets
│   ├── css/styles.css
│   └── js/scripts.js
├── requirements.txt
├── Dockerfile
└── manage.py
```

---

## 📊 Data Collected

Each click captures:

| Category | Data Points |
|----------|-------------|
| **Location** | Country, Region, City, ZIP, Timezone, Lat/Lon |
| **Network** | IP Address, ISP, Organization, AS Number |
| **Security** | VPN/Proxy Detection, Hosting/Datacenter Detection |
| **Device** | Device Type, Brand, Browser, Browser Version |
| **System** | Operating System, OS Version, Language |
| **Request** | User Agent, Referrer URL, Timestamp |

---

## 📝 License

This project is for educational purposes only. Use responsibly and in compliance with applicable laws and regulations.

---

<p align="center">
  Built with ❤️ using Django
</p>
