from twilio.rest import TwilioRestClient, TwilioLookupsClient

# SendGrid
EMAIL_BACKEND = "sgbackend.SendGridBackend"
DEFAULT_FROM_EMAIL = "no-reply@AppleAndOranges.com"

# EMAIL Notification
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#TWILIO
TWILIO_ACCOUNT = "AC9c6bb99e50e924b439977948bfb90b9d"
TWILIO_TOKEN = "b7ecee11d08c17cc8fed118a03e605f8"
TWILIO_FROM_NUMBER = '9496823573'

# Initiate Twilio Client
TWILIO = TwilioRestClient(TWILIO_ACCOUNT, TWILIO_TOKEN)
TWILIO_LOOKUPS = TwilioLookupsClient(TWILIO_ACCOUNT, TWILIO_TOKEN)
