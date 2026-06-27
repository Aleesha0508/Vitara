import magic
from rest_framework import serializers
from .models import Report

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "pdf_file",
            "panel_type",
            "visit_date",
            "extracted_values",
            "findings",
            "summary",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "extracted_values",
            "findings",
            "summary",
            "created_at",
        ]

        def validate_pdf_file(self, file):
          # Extension check
          if not file.name.endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
          
          # Size check
          if file.size > MAX_FILE_SIZE:
            raise serializers.ValidationError("File size must not exceed 5MB.")
          
          # MIME type check (reads actual file bytes)
          mime = magic.from_buffer(file.read(2048), mime=True)
          file.seek(0)  # reset pointer after reading
          if mime != 'application/pdf':
              raise serializers.ValidationError("Invalid file type. Must be a real PDF.")
          
          return file
          
