from django.db import models
from django.conf import settings


class Report(models.Model):

    PANEL_CHOICES = [
        ("CBC", "Complete Blood Count"),
        ("LFT", "Liver Function Test"),
        ("KFT", "Kidney Function Test"),
        ("LIPID", "Lipid Profile"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports"
    )

    pdf_file = models.FileField(upload_to="reports/")

    panel_type = models.CharField(
        max_length=10,
        choices=PANEL_CHOICES
    )

    visit_date = models.DateField()

    extracted_values = models.JSONField(
        default=dict,
        blank=True
    )

    findings = models.JSONField(
        default=dict,
        blank=True
    )

    summary = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.panel_type}"