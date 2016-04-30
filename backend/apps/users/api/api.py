from djoser import views
from djoser import signals
from datetime import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from djoser.views import ActivationView
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import detail_route, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from push_notifications.models import APNSDevice, GCMDevice
from _commons.api.viewsets.mixins import MultiSerializerViewSetMixin, CustomErrorMessagesMixin
from _commons.api.serializers.fields import UploadSerializer
from .serializers import *
from .permissions import *
from .exceptions import *
from users.models import AppUser, Language, University
from tasks.models import *
from .. import *
from tasks.api.api import MyTasksListViewSet
from django.contrib.auth.tokens import default_token_generator

def encode_uid(pk):
    try:
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        return urlsafe_base64_encode(force_bytes(pk)).decode()
    except ImportError:
        from django.utils.http import int_to_base36
        return int_to_base36(pk)

class CustomLoginView(views.LoginView):
    serializer_class = CustomLoginSerializer

    def get_serializer_class(self):
        return CustomLoginSerializer

    def action(self, serializer):
        self.user = serializer.user
        Token.objects.filter(user=self.user).delete()
        return super().action(serializer)


class CustomRegistrationView(views.RegistrationView):
    serializer_class = CustomUserRegistrationSerializer

    def get_serializer_class(self):
        return CustomUserRegistrationSerializer

    def perform_create(self, serializer):
        print("\n\n in USER/API/API: creating new user: ")
        instance = serializer.save(university=serializer.university)
        token = default_token_generator.make_token(instance)
        uid = encode_uid(instance.pk)
        print("IN CustomRegistrationView: uid/token: ")
        print("activate/{}/{}\n\n".format(uid,token))
        signals.user_registered.send(
            sender=self.__class__, user=instance, request=self.request)
        self.post_save(obj=instance, created=True)


class CustomUserView(views.UserView):
    serializer_class = CustomUserSerializer


class CustomSetUsernameView(views.SetUsernameView):
    serializer_class = CustomSetUsernameSerializer

    def get_serializer_class(self):
        return CustomSetUsernameSerializer


class CustomSetPasswordView(views.SetPasswordView):
    serializer_class = CustomSetPasswordSerializer

    def get_serializer_class(self):
        return CustomSetPasswordSerializer


class CustomPasswordResetView(views.PasswordResetView):
    serializer_class = CustomPasswordResetSerializer

    def get_serializer_class(self):
        return CustomPasswordResetSerializer


class UserProfilesViewSet(
    MultiSerializerViewSetMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):

    queryset = AppUser.objects.all()
    serializer_class = UserProfileSerializer

    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('gender', 'languages')
    ordering_fields = ('date_joined',)
    search_fields = ('skills', 'major', 'standing', 'first_name', 'last_name', )
    ordering = ('date_joined',)

    @detail_route(methods=['POST'], permission_classes=[IsAuthenticated, ])
    @parser_classes((JSONParser,))
    def rate(self, request, *args, **kwargs):
        """Using for tasker to rate poster after task completed
        """
        serializer = PosterRatingSerializer(data=request.data)
        if serializer.is_valid():
            user = self.get_object()
            self.check_object_permissions(self.request, user)
            user.poster_rating_field.add(
                score=serializer.data['rating'],
                user=request.user,
                ip_address=request.META['REMOTE_ADDR']
            )
            return Response(self.get_serializer(user).data)


class UserUploadAvatarAPIView(generics.CreateAPIView, generics.DestroyAPIView, generics.GenericAPIView):
    # http://stackoverflow.com/questions/19468478/add-user-specific-fields-to-django-rest-framework-serializer
    permission_classes = (AllowAny,)
    serializer_class = UploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid():
            if 'upload' in request.data:

                user = self.request.user
                upload = request.data['upload']
                field = user.avatar
                field.delete()
                field.save(upload.name, upload)
                thumb = user.avatar_thumbnail
                thumb.delete()
                thumb.save('avatarthumbnail', upload)

                return Response({'url': field.url, 'thumbnail': thumb.url}, status=status.HTTP_201_CREATED)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if user.avatar:
            user.avatar.delete()
            user.avatar_thumbnail.delete()
            user.save()
        return Response(status=status.HTTP_200_OK)


class LanguageListViewSet( viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (AllowAny, )
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('name', )
    ordering = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UniversityListViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = (AllowAny, )
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)
    ordering = ('name',)
    # Return proned University List to reduce server load
    def get_queryset(self):
        # try:
        # Filter University by whether has task
        # return University.objects.filter(domain__in=[i.poster.university.domain for i in \
        #                             Task.objects.filter(Q(status=Task.Open))])
        # except TypeError:
        #     raise UTP0003_INVALID_AUTH_TOKEN
        
        # Filter University bt whether has user
        all_university = University.objects.all()
        university_with_students = set(i.university.name for i in AppUser.objects.all())
        return University.objects.filter(name__in=university_with_students)
        

class CustomActivationView(ActivationView):
    def action(self, serializer):
        serializer.user.is_email_verified = True
        return super().action(serializer)


class UserInvitationCodeView(generics.UpdateAPIView, generics.GenericAPIView):
    # http://stackoverflow.com/questions/19468478/add-user-specific-fields-to-django-rest-framework-serializer
    permission_classes = (AllowAny,)
    serializer_class = UserInvitationCodeSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            if 'invite_code' in request.data:
                User = get_user_model()
                user_with_code = User.objects.filter(invite_code=request.data['invite_code'].upper())
                if not user_with_code:
                    raise UTP0004_INVALID_CODE
                user_with_code = user_with_code[0]
                user_with_code.invite_code_counter += 1
                user_with_code.save()
        return Response(user_with_code.full_name)
