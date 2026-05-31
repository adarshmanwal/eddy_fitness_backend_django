from rest_framework import serializers

from .models import Member


class MemberSerializer(serializers.ModelSerializer):

    class Meta:

        model = Member

        fields = "__all__"

class AssignMemberCenterSerializer(serializers.Serializer):
    member_id = serializers.IntegerField()
    center_id = serializers.IntegerField(required=False, allow_null=True)