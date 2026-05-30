from rest_framework import serializers

from .models import Center
from members.models import Member
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


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member

        fields = [
            "id",
            "full_name",
            "mobile_number",
            "email",
            "membership_plan",
            "joining_date",
            "expiry_date",
            "emergency_contact",
        ]

class CenterSerializer(serializers.ModelSerializer):

    trainers = TrainerSerializer(
        many=True,
        read_only=True
    )

    members = MemberSerializer(
        source="member_set",
        many = True,
        read_only = True
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
            "members",
        ]