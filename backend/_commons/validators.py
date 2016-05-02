import twilio
from django.core.exceptions import ValidationError
from django.conf import settings

def validate_phone_number(value):
    """
    Using twilio lookup service validates phone number
    https://www.twilio.com/docs/api/rest/lookups
    :param value:
        number
    :return:
        raise exception if number is not valid
    """
    try:
        lookup = settings.TWILIO_LOOKUPS.phone_numbers.get(value, include_carrier_info=True)
        x = 1
    except twilio.rest.exceptions.TwilioRestException:
        raise ValidationError("Invalid phone number!")

    if lookup.carrier['type']!='mobile':
        raise ValidationError("Not a mobile phone number!")
