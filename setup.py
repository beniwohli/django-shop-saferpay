import os
from setuptools import setup, find_packages

def read(fname):
    # read the contents of a text file
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = 'django-shop-saferpay',
    version = '1.2.1',
    description = 'A django SHOP payment backend for SaferPay',
    long_description = read('README.rst'),
    author = 'Benjamin Wohlwend',
    author_email = 'piquadrat@gmail.com',
    url = 'https://github.com/piquadrat/django-shop-saferpay',
    packages = find_packages(),
    zip_safe=False,
    include_package_data = True,
    install_requires=[
        'Django>=1.2',
        'django-shop',
        'requests',
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ]
)
