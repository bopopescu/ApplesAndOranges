from rest_framework import serializers


class ValidationErrorMixin(object):

    def is_valid(self, raise_exception=False):
        return super().is_valid(True)


class UnknownFieldsValidationMixin(object):

    def validate(self, attrs):
        """
        Used to raise an exception in the case submitted 'unknown' fields in json request body
        Also we don't allow sender to modify values of receiver

        :param attrs:
            valid fields
        :return:
            attrs or raises Validation exception
        """
        has_unknown_fields = set(self.initial_data.keys()) - set(attrs.keys())

        if has_unknown_fields:
            raise serializers.ValidationError("Unknown fields submitted: " + str(has_unknown_fields))

        return super().validate(attrs)