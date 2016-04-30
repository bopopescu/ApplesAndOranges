import pytz, json
from django.utils.functional import SimpleLazyObject
from django.utils import timezone
from django.http import HttpResponse, Http404
from rest_framework import status
from cacheops import cache
from cacheops import CacheMiss

class TimezoneMiddleware(object):

    def process_request(self, request):
        try:
            tzname = request.META.get('HTTP_USER_TIMEZONE', None)
            if tzname:
                timezone.activate(pytz.timezone(tzname))
                request.timezone = pytz.timezone(tzname)
        except pytz.UnknownTimeZoneError:
            return HttpResponse(
                json.dumps({"details": "Unknown timezone"}),
                content_type="application/json",
                status=status.HTTP_400_BAD_REQUEST
            )

