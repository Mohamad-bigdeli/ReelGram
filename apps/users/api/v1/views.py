from rest_framework.views import APIView
from ...services.user_service import UserService
from .serializers import UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework import status

class UserRegistrationAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_service = UserService()
            user = user_service.register_user(
                email=serializer.validated_data["email"],
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"]
            )
            return Response({"detail":{
                "status":"successful", 
                "user":{
                    "id":user.id,
                    "email":user.email,
                    "username":user.username
                },
                # access and refresh token 
            }}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail":{
                "status":"failed",
                "error":f"{e}"
            }}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)