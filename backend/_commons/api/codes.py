from copy import copy
from _commons.api.exceptions import PermissionCodeError, APIException, BusinessLogicError
from rest_framework.exceptions import ValidationError

class GenericErrorCode(object):
    def __getattr__(self, item):
        raise ValidationError({"detail": "Undefined error code {} supplied".format(item)})


def error(code=None, msg=None, **kwargs):

    if not isinstance(code, dict):
        raise ValueError('Code is required and should be of dict type')

    if code:
        message = msg if msg else code.get('message', None)
        handler = code.get('handler', None)
        payload = copy(code)

        # remove message and handler from the list
        del payload['message']
        del payload['handler']
        payload.update(kwargs)

        # if handler is not defined - use default APIException
        if not handler:
            handler = APIException

        # if APIException, then hide additional payload
        if handler==APIException:
            return handler(message)
        else:
            return handler(message, **payload)

    raise ValueError('Code {} is not defined!'.format(code))
