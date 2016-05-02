from rest_framework import serializers
from django.utils import timezone
from .mixins import *

class DateTimeFieldWihTZ(serializers.DateTimeField):

    def enforce_timezone(self, value):
        """
        When `self.default_timezone` is `None`, always return naive datetimes.
        When `self.default_timezone` is not `None`, always return aware datetimes.
        """
        try:
            tz = timezone._active.value
            if (self.default_timezone is not None) and not timezone.is_aware(value):
                return timezone.make_aware(value, tz)
            return value
        except AttributeError:
           return super().enforce_timezone(value)


    def to_representation(self, value):
        #timezone = get_current_timezone()
        value = timezone.localtime(value)
        return super().to_representation(value)


class MonthYearField(serializers.DateTimeField):

    def to_representation(self, value):
        # Return url including domain name.
        return value.strftime('%b %Y')


class UploadSerializer(ValidationErrorMixin, serializers.Serializer):
    upload = serializers.ImageField(required=True)