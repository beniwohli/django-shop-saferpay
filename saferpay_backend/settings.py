from django.conf import settings

ACCOUNT_ID = getattr(settings, 'SAFERPAY_ACCOUNT_ID', False)
ACCOUNT_PASSWORD = getattr(settings, 'SAFERPAY_ACCOUNT_PASSWORD', False)

NOTIFY_ADDRESS = getattr(settings, 'SAFERPAY_NOTIFY_ADDRESS', None)
ALLOW_COLLECT = getattr(settings, 'SAFERPAY_ALLOW_COLLECT', False)
DELIVERY = getattr(settings, 'SAFERPAY_DELIVERY', False)

CANCEL_URL_NAME = getattr(settings, 'SAFERPAY_CANCEL_URL_NAME', 'saferpay-cancel')
FAILURE_URL_NAME = getattr(settings, 'SAFERPAY_FAILURE_URL_NAME', 'saferpay-failure')

### Styling ###

BODYCOLOR = getattr(settings, 'SAFERPAY_BODY_COLOR', None)
HEADCOLOR = getattr(settings, 'SAFERPAY_HEADER_COLOR', None)
HEADLINECOLOR = getattr(settings, 'SAFERPAY_HEADLINE_COLOR', None)
MENUCOLOR = getattr(settings, 'SAFERPAY_MENU_COLOR', None)
BODYFONTCOLOR = getattr(settings, 'SAFERPAY_FONT_COLOR', None)
HEADFONTCOLOR = getattr(settings, 'SAFERPAY_HEAD_FONT_COLOR', None)
MENUFONTCOLOR = getattr(settings, 'SAFERPAY_MENU_FONT_COLOR', None)
FONT = getattr(settings, 'SAFERPAY_FONT_FACE', None)

### URLs ###

PROCESS_URL = getattr(settings, 'SAFERPAY_PROCESS_URL', 'https://www.saferpay.com/hosting/CreatePayInit.asp')
VERIFY_URL = getattr(settings, 'SAFERPAY_VERIFY_URL', 'https://www.saferpay.com/hosting/VerifyPayConfirm.asp')
PAYMENT_COMPLETE_URL = getattr(settings, 'SAFERPAY_PAYMENT_COMPLETE_URL', 'https://www.saferpay.com/hosting/PayComplete.asp')
USE_PAYMENT_COMPLETE_URL = getattr(settings, 'SAFERPAY_USE_PAYMENT_COMPLETE_URL', False)

USE_CELERY = getattr(settings, 'SAFERPAY_USE_CELERY', False)
