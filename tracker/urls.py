from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.home, name='home'),
    path('view/p/<uuid:uuid>/', views.track_view, name='track_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<uuid:uuid>/', views.detail, name='detail'),
    path('dashboard/<uuid:uuid>/download/', views.download_pdf, name='download_pdf'),
]
