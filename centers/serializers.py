from rest_framework import serializers

from .models import Center
from accounts.models import User


class TrainerSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]


class CenterSerializer(serializers.ModelSerializer):

    trainers = TrainerSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Center

        fields = [
            "id",
            "name",
            "address",
            "city",
            "state",
            "phone",
            "created_at",
            "updated_at",
            "trainers",
        ]