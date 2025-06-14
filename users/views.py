from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import AccountActivationTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect


def generate_account_activation_link(request, user):
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = AccountActivationTokenGenerator().make_token(user)

    return f'{domain}/users/activate/{uid}/{token}'


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            print(request.data)
            print(serializer.validated_data)
            print(serializer.data)
            user_data = serializer.validated_data
            user_data.pop('confirm_password')
            user = User(is_active=False, **user_data)
            user.set_password(user_data.get('password'))
            user.save()
            link = generate_account_activation_link(request, user)
            if user.email:
                send_mail(
                    recipient_list=[
                        user.email
                    ],
                    message=f'activate account with this link {link}'
                )
            return Response(serializer.data)
        return Response(serializer.errors)

@api_view(['GET'])
def activate(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
        if AccountActivationTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'activated':'True'})  # Redirect to login page after activation
        else:
            return Response({'activated':'False'})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'activated':'False'})