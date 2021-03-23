from django.urls import path
from .views import RegisterView, LoginAPIView, ForgotPasswordView, VerifyEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name = "register"),
    path('email-verify/<str:pk>/', VerifyEmailView.as_view(), name="email-verify"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('forgotpass/',ForgotPasswordView.as_view(), name = 'ForgetPass'),


]