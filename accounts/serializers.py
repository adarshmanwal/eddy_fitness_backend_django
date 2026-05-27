from rest_framework import serializers
from .models import User
from centers.models import Center
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "password",
            "role"
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role=validated_data["role"]
        )

        return user
    
class AssignTrainerCenterSerializer(serializers.Serializer):

    trainer_id = serializers.IntegerField()

    center_id = serializers.IntegerField()

class TrainerListSerializer(serializers.ModelSerializer):

    centers = serializers.StringRelatedField(
        many=True
    )

    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "centers",
        ]

class CenterSerializer(serializers.ModelSerializer):

    class Meta:

        model = Center

        fields = [
            "id",
            "name"
        ]


class TrainerListSerializer(serializers.ModelSerializer):

    centers = CenterSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "centers",
        ]