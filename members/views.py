from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Member
from .serializers import MemberSerializer

from centers.models import Center


class MemberListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role == "ADMIN":

            members = Member.objects.all()

        else:

            members = Member.objects.filter(
                center__in=request.user.centers.all()
            )

        serializer = MemberSerializer(
            members,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        center_id = request.data.get("center")

        try:

            center = Center.objects.get(id=center_id)

        except Center.DoesNotExist:

            return Response(
                {"error": "Center not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Trainer restriction
        if request.user.role == "TRAINER":

            if center not in request.user.centers.all():

                return Response(
                    {
                        "error":
                        "You cannot add members to this center"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = MemberSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MemberDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:

            return Member.objects.get(pk=pk)

        except Member.DoesNotExist:

            return None

    def get(self, request, pk):

        member = self.get_object(pk)

        if not member:

            return Response(
                {"error": "Member not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.role == "TRAINER":

            if member.center not in request.user.centers.all():

                return Response(
                    {"error": "Access denied"},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = MemberSerializer(member)

        return Response(serializer.data)

    def put(self, request, pk):

        member = self.get_object(pk)

        if not member:

            return Response(
                {"error": "Member not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.role == "TRAINER":

            if member.center not in request.user.centers.all():

                return Response(
                    {"error": "Access denied"},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = MemberSerializer(
            member,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        if request.user.role != "ADMIN":

            return Response(
                {"error": "Only admin can delete members"},
                status=status.HTTP_403_FORBIDDEN
            )

        member = self.get_object(pk)

        if not member:

            return Response(
                {"error": "Member not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        member.delete()

        return Response(
            {"message": "Member deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )