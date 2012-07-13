SaferPay backend for django SHOP
================================

This package provides a SaferPay backend for django SHOP

Installation
------------

 * Add ``'saferpay_backend',`` to your ``INSTALLED_APPS``
 * add ``'saferpay_backend.saferpay.SaferPayBackend',`` to ``SHOP_PAYMENT_BACKENDS``
 * set ``SAFERPAY_ACCOUNT_ID`` and ``SAFERPAY_ACCOUNT_PASSWORD`` to the values
   corresponding to your SaferPay account

There are a number of additional settings available. Please refer to 
``saferpay_backend/settings.py``.
