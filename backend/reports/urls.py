from django.urls import path
from .views import UploadReportView, ReportListView

urlpatterns = [
    path("", UploadReportView.as_view(), name="upload-report"),
    path('', ReportListView.as_view()),
]