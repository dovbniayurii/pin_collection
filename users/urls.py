from django.urls import path
from .views import call_task,SaveFCMToken,SignupView, VerifyPhoneNumber,SigninView, ResetPasswordView,ForgotPasswordView,VerifyOTPView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('verify-phone-number/', VerifyPhoneNumber.as_view(), name='verify-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('save-fcm-token/', SaveFCMToken.as_view(), name='save_fcm_token'),
    path('call-task/', call_task, name='call_task'),
    
    path('gettoken/', TokenObtainPairView.as_view(), name="get_token"),
    path('refreshtoken/', TokenRefreshView.as_view(), name="refresh_token"),
    path('verifytoken/', TokenVerifyView.as_view(), name="verify_token"),
]
