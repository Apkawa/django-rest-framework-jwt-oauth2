# coding: utf-8
# !/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages

version = '0.0.1'

if sys.argv[-1] == 'publish':
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[1] == 'bumpversion':
    print("bumpversion")
    try:
        part = sys.argv[2]
    except IndexError:
        part = 'patch'

    os.system("bumpversion --config-file setup.cfg %s" % part)
    os.system("git push --tags")
    sys.exit()

__doc__ = """A generic api for oauth2"""

project_name = 'django-rest-framework-jwt-oauth2'
app_name = 'rest_framework_jwt_oauth2'

ROOT = os.path.dirname(__file__)


def read(fname):
    return open(os.path.join(ROOT, fname)).read()


setup(
    name=project_name,
    version=version,
    description=__doc__,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url="https://githib.com/Apkawa/django-rest-framework-jwt-oauth2",
    author="Apkawa",
    author_email='apkawa@gmail.com',
    packages=[package for package in find_packages() if package.startswith(app_name)],
    install_requires=['six'],
    zip_safe=False,
    include_package_data=True,
    keywords=['django'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
