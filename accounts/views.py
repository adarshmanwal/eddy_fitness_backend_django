from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, TrainerListSerializer, AssignTrainerCenterSerializer, TrainerUpdateSerializer

from .models import User

from centers.models import Center

from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminUserRole

class RegisterView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            if serializer.validated_data.get("role") != "TRAINER":

                return Response(
                    {"error": "Only TRAINER accounts can be registered"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class LoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:

            return Response(
                {"error": "Invalid Credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
    
class AssignTrainerCenterView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def post(self, request):
        serializer = AssignTrainerCenterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        trainer_id = serializer.validated_data["trainer_id"]
        center_ids = serializer.validated_data["center_id"]  # list, can be []

        try:
            trainer = User.objects.get(id=trainer_id, role="TRAINER")
        except User.DoesNotExist:
            return Response({"error": "Trainer not found"}, status=status.HTTP_404_NOT_FOUND)

        # if centers list is empty => unassign from all
        if not center_ids:
            trainer.centers.clear()
            return Response({"message": "Trainer unassigned from all centers"}, status=status.HTTP_200_OK)

        centers = Center.objects.filter(id__in=center_ids)

        # validate all centers exist
        found_ids = set(centers.values_list("id", flat=True))
        missing_ids = [cid for cid in center_ids if cid not in found_ids]
        if missing_ids:
            return Response(
                {"error": "Center not found", "missing_center_ids": missing_ids},
                status=status.HTTP_404_NOT_FOUND
            )

        # IMPORTANT: this replaces existing centers with the new list (removes the rest)
        trainer.centers.set(centers)

        return Response({"message": "Trainer centers updated successfully"}, status=status.HTTP_200_OK)
class UnassignTrainerCenterView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def post(self, request):
        serializer = AssignTrainerCenterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        trainer_id = serializer.validated_data["trainer_id"]
        center_id = serializer.validated_data["center_id"]

        try:
            trainer = User.objects.get(id=trainer_id, role="TRAINER")
        except User.DoesNotExist:
            return Response({"error": "Trainer not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            center = Center.objects.get(id=center_id)
        except Center.DoesNotExist:
            return Response({"error": "Center not found"}, status=status.HTTP_404_NOT_FOUND)

        # send 404 if trainer is NOT assigned to this center
        if not trainer.centers.filter(id=center.id).exists():
            return Response(
                {"error": "Trainer is not assigned to this center"},
                status=status.HTTP_404_NOT_FOUND
            )

        trainer.centers.remove(center)

        return Response({"message": "Center unassigned successfully"}, status=status.HTTP_200_OK)
    

class TrainerListView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminUserRole
    ]

    def get(self, request):

        trainers = User.objects.filter(
            role="TRAINER"
        ).prefetch_related("centers")

        serializer = TrainerListSerializer(
            trainers,
            many=True
        )

        return Response(serializer.data)

class TrainerDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]  # ADMIN only

    def get_object(self, id):
        try:
            return User.objects.prefetch_related("centers").get(id=id, role="TRAINER")
        except User.DoesNotExist:
            return None

    def get(self, request, id):
        trainer = self.get_object(id)
        if trainer is None:
            return Response({"error": "Trainer not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(TrainerListSerializer(trainer).data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        trainer = self.get_object(id)
        if trainer is None:
            return Response({"error": "Trainer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TrainerUpdateSerializer(trainer, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        # return updated trainer profile (including centers)
        trainer.refresh_from_db()
        return Response(TrainerListSerializer(trainer).data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        trainer = self.get_object(id)
        if trainer is None:
            return Response({"error": "Trainer not found"}, status=status.HTTP_404_NOT_FOUND)

        trainer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)