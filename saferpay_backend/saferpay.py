import urlparse

from django.conf.urls.defaults import patterns, url
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import get_language, ugettext_lazy as _

from shop.models.ordermodel import Order
import requests

from saferpay_backend import settings
from saferpay_backend.tasks import payment_complete
import logging

logger = logging.getLogger('shop.payment.saferpay')


class SaferPayBackend(object):
    backend_name = "SaferPay"
    url_namespace = "saferpay"

    backend_description = _('credit card')

    def __init__(self, shop):
        self.shop = shop

    def pay(self, request):
        protocol = 'https' if request.is_secure() else 'http'
        shop = self.shop
        order = shop.get_order(request)
        order.status = Order.PAYMENT
        order.save()
        domain = '%s://%s/%s' % (protocol, Site.objects.get_current().domain, get_language())
        data = {
            'AMOUNT': int(shop.get_order_total(order) * 100),
            'CURRENCY': 'CHF', # TODO: don't hard code this
            'DESCRIPTION': shop.get_order_short_name(order),
            'LANGID': get_language()[:2],
            'ALLOWCOLLECT': 'yes' if settings.ALLOW_COLLECT else 'no',
            'DELIVERY': 'yes' if settings.DELIVERY else 'no',
            'ACCOUNTID': settings.ACCOUNT_ID,
            'ORDERID': shop.get_order_unique_id(order),
            'SUCCESSLINK': domain +  reverse('saferpay-verify'),
            'BACKLINK': domain + reverse(settings.CANCEL_URL_NAME),
            'FAILLINK': domain + reverse(settings.FAILURE_URL_NAME),
            
        }
        for style in ('BODYCOLOR', 'HEADCOLOR', 'HEADLINECOLOR', 'MENUCOLOR', 'BODYFONTCOLOR', 'HEADFONTCOLOR', 'MENUFONTCOLOR', 'FONT'):
            style_value = getattr(settings, style)
            if style_value is not None:
                data[style] = style_value
        
        response = requests.get(settings.PROCESS_URL, params=data)
        logger.info('Saferpay: order %d\tredirected to saferpay gateway', order.pk)
        return HttpResponseRedirect(response.content)

    def verify(self, request):
        order = self.shop.get_order(request)
        if not order:
            return self.failure(request)
        data = {
            'SIGNATURE': request.GET.get('SIGNATURE', ''),
            'DATA': request.GET.get('DATA', ''),
        }
        logger.info('Saferpay: order %i\tverifying , DATA: %s, SIGNATURE %s', order.pk, data['DATA'], data['SIGNATURE'])
        response = requests.get(settings.VERIFY_URL, params=data)
        if response.status_code == 200 and response.content.startswith('OK'):
            response_data = urlparse.parse_qs(response.content[3:])
            transaction_id = response_data['ID'][0]
            self.shop.confirm_payment(order, self.shop.get_order_total(order), transaction_id, self.backend_name)
            params = {'ACCOUNTID': settings.ACCOUNT_ID, 'ID': transaction_id, 'spPassword': settings.ACCOUNT_PASSWORD}
            logger.info('Saferpay: order %i\ttransaction: %s\tpayment verified', order.pk, transaction_id)
            if settings.USE_CELERY:
                payment_complete.delay(params=params, order_id=order.pk)
            else:
                try:
                    payment_complete(params=params, order_id=order.pk)
                except Exception:
                    pass # this is already logged in payment_complete
            order.save()  # force order.modified to be bumped (we rely on this in the "thank you" view)
            return self.success(request)
        return self.failure(request)

    def cancel(self, request):
        order = self.shop.get_order(request)
        if not order:
            raise Http404
        return render_to_response('saferpay_backend/cancel.html', {
            'order': self.shop.get_order(request),
            'order_name': self.shop.get_order_short_name(order)
        }, context_instance=RequestContext(request))

    def failure(self, request):
        order = self.shop.get_order(request)
        if not order:
            raise Http404
        return render_to_response('saferpay_backend/failure.html', {
             'order': order,
             'order_name': self.shop.get_order_short_name(order)
        }, context_instance=RequestContext(request))

    def success(self, request):
        return HttpResponseRedirect(self.shop.get_finished_url())

    def get_urls(self):
        return patterns('',
            url(r'^$', self.pay, name='saferpay'),
            url(r'^v/$', self.verify, name='saferpay-verify'),
            url(r'^c/$', self.cancel, name='saferpay-cancel'),
            url(r'^f/$', self.failure, name='saferpay-failure'),
        )
