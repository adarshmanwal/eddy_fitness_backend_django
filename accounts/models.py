from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("TRAINER", "Trainer"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    centers = models.ManyToManyField(
        "centers.Center",
        blank=True,
        related_name="trainers"
    )