from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (GenericAPIView,
                                     ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.views import APIView

from .serializers import RegisterSerializer
from .models import User, Request
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import AccountActivationTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .serializers import UserSerializer
from posts.models import Post
from posts.serializers import PostListSerializer
from posts.pagination import PostPagination

def generate_account_activation_link(request, user):
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = AccountActivationTokenGenerator().make_token(user)

    return f'{domain}/users/activate/{uid}/{token}'


class RegisterView(GenericAPIView):
    permission_classes = []
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user_data.pop('confirm_password')
            user = User(is_active=False, **user_data)
            user.set_password(user_data.get('password'))
            user.save()
            link = generate_account_activation_link(request, user)
            if user.email:
                send_mail(
                    subject='Activate you account',
                    from_email=settings.EMAIL_HOST_USER,
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
            return Response({'activated':'True'})
        else:
            return Response({'activated':'False'})
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'activated':'False'})

class UsersListApiView(ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserPostsListApiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        return self.queryset.filter(author_id=self.kwargs.get('pk'))

@api_view(['POST'])
def send_follow_request(request, pk):
    to_user = User.objects.get(id=pk)
    request = Request(from_user=request.user, to_user=to_user)
    request.save()
    return Response({'request has been sent'})

class RequestsDetailApiView(APIView):
    def get_follow_request(self, request, request_pk):
        follow_request = Request.objects.filter(
            pk=request_pk, to_user=request.user)
        if follow_request.exists():
            return  follow_request.first()

    def post(self, request, *args, **kwargs ):
        follow_request = self.get_follow_request(request, kwargs.get('request_pk'))
        if follow_request:
            follow_request.accept()
            return Response({"message": 'accepted'})
        return Response({'message': 'Not Found'}, status=404)

    def put(self, request, *args, **kwargs ):
        follow_request = self.get_follow_request(request, kwargs.get('request_pk'))
        if follow_request:
            follow_request.follow_back()
            return Response({"message": 'followed back'})
        return Response({'message': 'Not Found'}, status=404)

    def delete(self, request, *args, **kwargs ):
        follow_request = self.get_follow_request(request, kwargs.get('request_pk'))
        if follow_request:
            follow_request.reject()
            return Response({"message": 'rejected'})
        return Response({'message': 'Not Found'}, status=404)
