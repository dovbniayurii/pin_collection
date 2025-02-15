from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSignupSerializer, UserSigninSerializer
from .models import CustomUser,OTP
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ResetPasswordSerializer,OTPVerificationSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSignupSerializer, UserSigninSerializer, ForgotPasswordSerializer, OTPVerificationSerializer, ResetPasswordSerializer
from django.core.mail import send_mail
from django.conf import settings

class SignupView(APIView):
    @swagger_auto_schema(
        request_body=UserSignupSerializer,
        responses={201: openapi.Response("User created successfully")},
    )
    def post(self, request):
        """
        User Signup API
        
        Creates a new user.
        """
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    @swagger_auto_schema(
        request_body=UserSigninSerializer,
        responses={200: openapi.Response("Returns user authentication tokens")},
    )
    def post(self, request):
        """
        User Signin API
        
        Authenticates a user and returns a JWT token.
        """
        serializer = UserSigninSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(APIView):
    @swagger_auto_schema(
        request_body=ForgotPasswordSerializer,
        responses={200: openapi.Response("OTP sent to email")},
    )
    def post(self, request):
        """
        Forgot Password API
        
        Sends an OTP to reset the password.
        """
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(useremail=email)
            except CustomUser.DoesNotExist:
                return Response({"error": "User with this email doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
            
            otp_instance = OTP.generate_otp(user)
            send_mail(
                subject="Reset Your Password",
                message=f"Your OTP for password reset is: {otp_instance.otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    @swagger_auto_schema(
        request_body=OTPVerificationSerializer,
        responses={200: openapi.Response("OTP verified successfully")},
    )
    def post(self, request):
        """
        Verify OTP API
        
        Verifies the OTP and returns an authentication token.
        """
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            otp_value = serializer.validated_data['otp']
            email = serializer.validated_data['email']
            
            try:
                user = CustomUser.objects.get(useremail=email)
            except CustomUser.DoesNotExist:
                return Response({"email": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            otp_instance = OTP.objects.filter(user__useremail=email, otp=otp_value).order_by('-created_at').first()

            if not otp_instance:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
            
            if otp_instance.is_expired():
                return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            otp_instance.delete()
            
            return Response({
                "message": "OTP verified successfully.",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'useremail': user.useremail,
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Reset Password API\n\nResets the user's password after verifying the OTP. User must be authenticated with JWT token.",
        request_body=ResetPasswordSerializer,
        responses={200: "Password reset successfully"},
    )
    def post(self, request):
        """
        Reset Password API
        
        Resets the user password after OTP verification.
        """
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
