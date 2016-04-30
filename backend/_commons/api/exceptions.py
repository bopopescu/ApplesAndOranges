from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework import exceptions


HTTP_422_BUSINESS_LOGIC = 422


class CustomAPIException(APIException):
    code = None
    message = None
    internal = None
    more_info = None

    def __init__(self, message=None, extra_payload={}, **kwargs):
        super().__init__(message, **kwargs)
        detail = {'code': self.__class__.__name__}
        if self.message:
            detail['detail'] = self.message
        if message:  # passed when raising exception
            detail['detail'] = message
        if self.internal:
            detail['internal'] = self.internal
        if self.more_info:
            detail['more_info'] = self.more_info

        detail.update(extra_payload)

        self.detail = detail
        print('CustomAPIException:', self.detail)


class BusinessLogicError(CustomAPIException):
    status_code = HTTP_422_BUSINESS_LOGIC
    code = "ETB0000"


class PermissionCodeError(CustomAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "ETP0000"
    message = "You are not allowed to perform this action"


class InternalInfoMixin(object):
    internal = "This means..."
    more_info = "https://drive.google.com/drive/u/0/folders/0B8WnfaHtXP4QfkgxZ1hEcUJTN0VsbHgweXNuMG1jZlpIbHJRUlIxZXhOb0JTdmNpbWg4OGM"

    
def custom_exception_handler(exc, context):
    if isinstance(exc, exceptions.ValidationError):
        exc.detail = {
                'data': exc.detail,
                'detail': 'Unfortunately, there are some problems with the data you committed'
            }

    return exception_handler(exc, context)
