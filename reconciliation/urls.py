
from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_transactions, name="upload_transactions"),
    path("exceptions/", views.exception_management, name="exception_management"),
    path("download-report/", views.download_report, name="download_report"),
]
