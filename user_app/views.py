from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken
from .models import User
from .serializers import UserSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        password_confirm = data.get("password_confirm", None)

        if password_confirm is None:
            raise exceptions.ValidationError(
                {"password_confirm": "Please add password confirm"}
            )

        if data["password"] != password_confirm:
            raise exceptions.ValidationError(
                {"password_confirm": "Passwords not matched"}
            )

        if User.objects.filter(email=data["email"]).exists():
            raise exceptions.ValidationError({"email": "Email already exists"})

        serializer = UserSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Generate JWT tokens
        access_token = str(AccessToken.for_user(user))

        return Response(
            {
                "user": serializer.data,
                "access": access_token,
            }
        )
