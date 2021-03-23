import data as data
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer,  ForgotSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, VerifyEmail
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated

from .utils import Util, PasswordChange


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            uid = user_data['uid']
            user = User.objects.get(email=user_data['email'])

            current_site = get_current_site(request).domain
            relativeLink = "/auth/email-verify/"
            absurl = 'http://' + current_site + relativeLink + str(user.uid)
            email_body = 'Hi ' + "User" + ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}
            Util.send_email(data)

            content = {'Verification link send to email, verify your account',uid}

            return PasswordChange.verify_email(content, status=status.HTTP_200_OK)



class VerifyEmailView(generics.GenericAPIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(uid=pk)
            user.is_verified = True
            user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"Not a valid token"}, status= status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        # user = User.objects.get(email=request.data.email)
        user = User.objects.get(email=self.request.data['email'])
        # if not user:
        #     raise AuthenticationFailed('user not registered')
        #
        # if not user.is_active:
        #     raise AuthenticationFailed('Account disabled, contact admin')
        #
        # if not user.is_verified:
        #     raise AuthenticationFailed('Email is not verified')


        token = RefreshToken.for_user(user)
        serializer = LoginSerializer(user)
        _data = serializer.data
        _data.update({'token': str(token.access_token)})
        # del _data['password']
        user.is_active = True
        user.save()
        # return ({, 'message': 'Login Successful'})
        print(token)


        # serializer = self.serializer_class(data = request.data)
        # serializer.is_valid(raise_exception=True)
        print(serializer.data)
        return Response(_data)

        try:
            User.objects.filter(is_active = request.data['email'] )
            return Response(status= status.HTTP_200_OK)
        except:
            pass

            return Response(serializer.data, status=status.HTTP_200_OK)


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotSerializer
    def post(self, request):
        try:
            user = self.request.data
            #print(user)
            #import pdb
            #pdb.set_trace()

            if not user.get('email'):
                return Response(f"email is required", status=status.HTTP_400_BAD_REQUEST)

            _user = User.objects.get(email = self.request.data['email'])
            serializer = ForgotSerializer(user)
            data_ = serializer.data
            relativeLink = "/auth/change-pass/"

            return PasswordChange.verify_email(request, _user, data_, relativeLink)

        except:
            return Response({"User Not Found"}, status=status.HTTP_400_BAD_REQUEST)







class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, pk):
        try:
            for field in ['confirm_pass', 'password']:
                if not self.request.data.get(field):
                    return Response({f"{field} is required"}, status.HTTP_400_BAD_REQUEST)
            if (self.request.data['password'] != self.request.data['confirm_pass']):
                return Response({"Password Dont Match"}, status.HTTP_400_BAD_REQUEST)

            _user = User.objects.get(uid=pk)
            _user.set_password(request.data['password'])
            _user.save()
            return Response({"status": True, "message": "password changed sucessfully", "data": {}},
                            status=status.HTTP_201_CREATED)

        except Exception:
            return Response({"User Not Found"}, status.HTTP_400_BAD_REQUEST)


class TokenTestingView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReadProjectSerializer

    def get(self, request):
        try:
            user = request.user
            serializer = ReadProjectSerializer(user)
            _data = serializer.data
            return Response({'data': _data})

        except User.DoesNotExist:
            return Response({"Not a valid token"}, status.HTTP_400_BAD_REQUEST)
