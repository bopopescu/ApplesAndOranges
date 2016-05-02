from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from djoser.serializers import LoginSerializer,\
    UserRegistrationWithAuthTokenSerializer, UserRegistrationSerializer, SetUsernameSerializer, \
    SetPasswordSerializer, PasswordResetSerializer
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from _commons.api.viewsets.mixins import CustomErrorMessagesMixin
from _commons.api.serializers.fields import DateTimeFieldWihTZ
from _commons.api.serializers import mixins
from users.models import Language, University
from _commons.api.exceptions import BusinessLogicError
from payments.api.serializers import CustomerSerializer
from .exceptions import *
from tasks.api.serializers import EarningsListSerializer
 
User = get_user_model()
 
 
class LanguageSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Language
        fields = ('id', 'name', )
 
 
class UniversitySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = University
        fields = ('id', 'name', 'domain', 'location')
 
 
class CustomLoginSerializer(LoginSerializer):
 
    def validate(self, attrs):
        self.user = authenticate(username=attrs[User.USERNAME_FIELD], password=attrs['password'])
        if self.user:
            # Remove check email verification:
            # Check email verification in user actions
            # if not self.user.is_email_verified:
            #     raise UTP0002_UNVARIFY_ACCOUNT
            if not self.user.is_active:
                raise UTP0002_SUSPENDED_ACCOUNT
            return attrs
        else:
            raise UTP0001_INVALID_LOGIN
 
    def to_internal_value(self, data):
        """
        This is solution to avoid case sensitive usernames/emails during login as Django's case sensitivenes is something
        they don't want to get rid of due to legacy issues
        :param data:
            submitted attributed
        :return:
            attributes where USERNAME_FIELD value is lowecase
        """
        if data.get(User.USERNAME_FIELD, None):
            data[User.USERNAME_FIELD]=data[User.USERNAME_FIELD].lower()
        return super().to_internal_value(data)
 
class CustomUserRegistrationSerializer(
        CustomErrorMessagesMixin,
        UserRegistrationWithAuthTokenSerializer):
 
    birthday = serializers.DateField(required=False)
 
    class Meta:
        model = User
        fields = UserRegistrationSerializer.Meta.fields + ('auth_token', 'university', 'birthday',)
        # print('CustomUserRegistrationSerializer', fields)
        write_only_fields = ('password',)
        extra_kwargs = {'email': {'required': True}}
 
        custom_error_messages_for_validators = {
            'username': {
                UniqueValidator: _('This username is already being used, please select another one'),
            },
            'email': {
                UniqueValidator: _('This email is already being used.'),
            }
        }
 
    def validate_email(self, email):
        domain = email.split('@')[1]
        try:
            self.university = University.objects.get(domain=domain.lower())
        except University.DoesNotExist:
            raise UTB0001_INVALID_EMAIL(extra_payload={
                'intenal': ['@'+u.domain for u in University.objects.all()]
            })
        return email
 
    def to_internal_value(self, data):
        """
        This is solution to avoid case sensitive usernames/emails during login as Django's case sensitivenes is something
        they don't want to get rid of due to legacy issues
        :param data:
            submitted attributed
        :return:
            attributes where USERNAME_FIELD value is lowecased
        """
        if data.get(User.USERNAME_FIELD, None):
            data[User.USERNAME_FIELD] = data[User.USERNAME_FIELD].lower()
        return super().to_internal_value(data)
 
 
class CustomUserSerializer(serializers.ModelSerializer):
    # customer = CustomerSerializer(read_only=True)
    university_name = serializers.CharField(source='university.name', read_only=True)
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User._meta.pk.name,
            User.USERNAME_FIELD,
            'university_name',
        ) + User.CUSTOM_FIELDS
        read_only_fields = User.READ_ONLY_FIELDS
 
 
class CustomSetUsernameSerializer(mixins.ValidationErrorMixin, SetUsernameSerializer):
    pass
 
 
class CustomSetPasswordSerializer(mixins.ValidationErrorMixin, SetPasswordSerializer):
    default_detail = ''
    default_error_messages = {
        'invalid_password': 'You provided incorrect current password',
    }
 
 
class CustomPasswordResetSerializer(mixins.ValidationErrorMixin, PasswordResetSerializer):
    pass
 
 
# TODO: Move it to _commons
# class UploadSerializer(mixins.ValidationErrorMixin, serializers.Serializer):
#     upload = serializers.ImageField(required=True)
 
 
class UserProfileSerializer(serializers.ModelSerializer):
 
    languages = LanguageSerializer(many=True, read_only=True)
    date_joined = DateTimeFieldWihTZ(read_only=True)
 
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'phone', 'personal_email', 'avatar', 'avatar_thumbnail', 
                  'age', 'skills', 'major', 'standing', 'about', 'languages', 'date_joined', 'university',
                  'poster_rating', 'tasker_rating')
 
 
class PosterRatingSerializer(mixins.ValidationErrorMixin, serializers.Serializer):
    rating = serializers.ChoiceField(required=True, choices=[-1, 1],
        error_messages={
            'invalid_choice': '"{input}" is not a valid choice. Valid choices are (-1; 1)'
        })

class UserInvitationCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField()

