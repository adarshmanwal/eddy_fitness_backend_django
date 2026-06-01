from django.db import models


class Member(models.Model):

    full_name = models.CharField(max_length=255)

    mobile_number = models.CharField(max_length=15)

    email = models.EmailField()

    address = models.TextField()

    membership_plan = models.CharField(max_length=100)

    joining_date = models.DateField()

    expiry_date = models.DateField()

    emergency_contact = models.CharField(max_length=15)

    health_notes = models.TextField(
        blank=True,
        null=True
    )

    center = models.ForeignKey(
        "centers.Center",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.full_name