import logging

import requests

from saferpay_backend import settings

logger = logging.getLogger('shop.payment.saferpay')


celery_task = None
if settings.USE_CELERY:
    from celery import task as celery_task


def payment_complete(url=settings.PAYMENT_COMPLETE_URL, params=None, order_id=None):
    if params is None:
        params = {}
    if settings.USE_PAYMENT_COMPLETE_URL:
        try:
            response = requests.get(url, timeout=10, params=params)
            if response.ok:
                logger.info('Saferpay: order %i\tcompletion of payment SUCCEEDED', order_id)
                return response.content
            else:
                raise response.error
        except Exception, exc:
            if celery_task:
                payment_complete.retry(exc=exc, countdown=5*60)
            else:
                logger.error('Saferpay: order %i\tcompletion of payment FAILED', order_id)
                raise

if celery_task:
    payment_complete = celery_task.task(max_retries=None)(payment_complete)