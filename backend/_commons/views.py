from rest_framework.views import exception_handler as rest_exception_handler
from rest_framework import exceptions


def exception_handler(exc, context):
    if isinstance(exc, exceptions.ValidationError):
        exc.detail = {
                'data': exc.detail,
                'detail': 'Unfortunately, there are some problems with the data you committed'
            }
    return rest_exception_handler(exc, context)
