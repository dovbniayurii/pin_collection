from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSignupSerializer, UserSigninSerializer
from .models import PinUser,OTP,FCMToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ResetPasswordSerializer,OTPVerificationSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSignupSerializer, UserSigninSerializer, OTPSendSerializer, OTPVerificationSerializer, ResetPasswordSerializer
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
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_sms(phone_number, message):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return message.sid
    except TwilioRestException as e:
        print(f"Twilio Error: {e}")
        raise
    except Exception as e:
        print(f"General Error: {e}")
        raise

class ForgotPasswordView(APIView):
    @swagger_auto_schema(
        request_body=OTPSendSerializer,
        responses={200: openapi.Response("OTP sent successfully")},
    )
    def post(self, request):
        """
        Send OTP API

        Sends an OTP to the provided email or phone number.
        """
        print(request.data)
        serializer = OTPSendSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')

            user = None

            if email:
                try:
                    user = PinUser.objects.get(useremail=email)
                except PinUser.DoesNotExist:
                    return Response({"email": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            elif phone_number:
                try:
                    user = PinUser.objects.get(phone_number=phone_number)
                except PinUser.DoesNotExist:
                    return Response({"phone_number": "User with this phone number does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            otp_instance = OTP.generate_otp(user)

            if email:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP is: {otp_instance.otp}',
                    'no-reply@example.com',
                    [email],
                )
            elif phone_number:
                send_sms(phone_number, f'Your OTP is: {otp_instance.otp}')

            return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
        print(serializer.errors)
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
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')

            try:
                if email:
                    user = PinUser.objects.get(useremail=email)
                    otp_instance = OTP.objects.filter(user__useremail=email, otp=otp_value).order_by('-created_at').first()
                elif phone_number:
                    user = PinUser.objects.get(phone_number=phone_number)
                    otp_instance = OTP.objects.filter(user__phone_number=phone_number, otp=otp_value).order_by('-created_at').first()
                else:
                    return Response({"error": "Provide either email or phone number."}, status=status.HTTP_400_BAD_REQUEST)
            except PinUser.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

            if not otp_instance:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            if otp_instance.is_expired():
                return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)

            otp_instance.delete()

            return Response({
                "message": "OTP verified successfully.",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'useremail': user.useremail,
                'phone_number': user.phone_number
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



        
        
class SaveFCMToken(APIView):
    #permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        token = request.data.get('token')
        #user = request.user

        if not token:
            return Response({"error": "Token is required"}, status=400)

        # Update or create FCM token
        fcm_token, created = FCMToken.objects.update_or_create(
         #   user=user,
            defaults={"token": token}
        )

        return Response({"message": "Token saved successfully", "token": token})
    
    
from django.http import HttpResponse
from .tasks import my_task,send_morning_push_notification

def call_task(request):
    # Calling the task asynchronously
    send_morning_push_notification.delay()
    return HttpResponse("Task has been called!")