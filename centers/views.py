from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdminUserRole, IsAdminOrAssignedCenter

from .models import Center
from .serializers import CenterSerializer


class CenterListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get_permissions(self):

        if self.request.method == "POST":

            return [IsAuthenticated(), IsAdminUserRole()]

        return [IsAuthenticated()]

    def get(self, request):

        if request.user.role == "ADMIN":

            centers = Center.objects.all()

        else:

            centers = request.user.centers.all()

        serializer = CenterSerializer(
            centers,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = CenterSerializer(data=request.data)

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


class CenterDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_permissions(self):

        if self.request.method == "GET":

            return [IsAuthenticated(), IsAdminOrAssignedCenter()]

        return [IsAuthenticated(), IsAdminUserRole()]

    def get_object(self, pk):

        try:
            return Center.objects.get(pk=pk)

        except Center.DoesNotExist:
            return None

    def get(self, request, pk):

        center = self.get_object(pk)

        if not center:

            return Response(
                {"error": "Center not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, center)

        serializer = CenterSerializer(center)

        return Response(serializer.data)

    def put(self, request, pk):
        center = self.get_object(pk)

        if not center:

            return Response(
                {"error": "Center not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CenterSerializer(
            center,
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
        center = self.get_object(pk)

        if not center:

            return Response(
                {"error": "Center not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        center.delete()

        return Response(
            {"message": "Center deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )