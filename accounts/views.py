from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, TrainerListSerializer, AssignTrainerCenterSerializer

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

    permission_classes = [
        IsAuthenticated,
        IsAdminUserRole
    ]

    def post(self, request):

        serializer = AssignTrainerCenterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            trainer_id = serializer.validated_data["trainer_id"]

            center_id = serializer.validated_data["center_id"]

            try:

                trainer = User.objects.get(
                    id=trainer_id,
                    role="TRAINER"
                )

            except User.DoesNotExist:

                return Response(
                    {"error": "Trainer not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:

                center = Center.objects.get(id=center_id)

            except Center.DoesNotExist:

                return Response(
                    {"error": "Center not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            trainer.centers.add(center)

            return Response({
                "message": "Center assigned successfully"
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
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