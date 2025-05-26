import uuid
from django.db import models


class Candidate(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("checked", "Checked"),
        ("rejected", "Rejected")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default="pending")
    screening_log = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.full_name} ({self.status})"


class Check:

    def __init__(self, name: str, result: str) -> None:
        self.name = name
        self.result = result

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "result": self.result,
        }
