from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status


class Util:
    @staticmethod
    def send_email(data):
        email= EmailMessage(
            subject=data['email_subject'],body= data['email_body'],to=[data['to_email']]
        )
        email.send()

class PasswordChange:
    @staticmethod
    def verify_email(request, user, user_data, relativeLink):
        current_site = get_current_site(request).domain
        absurl = 'http://' + current_site + relativeLink + str(user.uid)
        email_body = 'Hi ' + "User" + \
                     ' Use the link below to reset password \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Reset password'}
        send_mail('click on the link', email_body, 'anubhajainit@gmail.com', [user.email], )
        return Response(user_data, status=status.HTTP_201_CREATED)

