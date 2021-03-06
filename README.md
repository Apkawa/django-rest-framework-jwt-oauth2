[![Build Status](https://travis-ci.org/Apkawa/django-rest-framework-jwt-oauth2.svg?branch=master)](https://travis-ci.org/Apkawa/django-rest-framework-jwt-oauth2)
[![Coverage Status](https://coveralls.io/repos/github/Apkawa/django-rest-framework-jwt-oauth2/badge.svg)](https://coveralls.io/github/Apkawa/django-rest-framework-jwt-oauth2)
[![codecov](https://codecov.io/gh/Apkawa/django-rest-framework-jwt-oauth2/branch/master/graph/badge.svg)](https://codecov.io/gh/Apkawa/django-rest-framework-jwt-oauth2)
[![Requirements Status](https://requires.io/github/Apkawa/django-rest-framework-jwt-oauth2/requirements.svg?branch=master)](https://requires.io/github/Apkawa/django-rest-framework-jwt-oauth2/requirements/?branch=master)
[![PyUP](https://pyup.io/repos/github/Apkawa/django-rest-framework-jwt-oauth2/shield.svg)](https://pyup.io/repos/github/Apkawa/django-rest-framework-jwt-oauth2)
[![PyPI](https://img.shields.io/pypi/pyversions/django-rest-framework-jwt-oauth2.svg)]()

Project for merging different file types, as example easy thumbnail image and unpacking archive in one field

# Installation

```bash
pip install django-rest-framework-jwt-oauth2

```

or from git

```bash
pip install -e git+https://githib.com/Apkawa/django-rest-framework-jwt-oauth2.git#egg=django-rest-framework-jwt-oauth2
```

## Django and python version

| Python<br/>Django |        3.5         |      3.6           |      3.7           |       3.8          |
|:-----------------:|--------------------|--------------------|--------------------|--------------------|
| 1.8               |       :x:          |      :x:           |       :x:          |      :x:           |
| 1.11              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |      :x:           |
| 2.2               | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| 3.0               |       :x:          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |



# Usage


# Contributing

## run example app

```bash
pip install -r requirements-dev.txt
./test/manage.py migrate
./test/manage.py runserver
```

## run tests

```bash
pip install -r requirements-dev.txt
pytest
tox
```

## Update version

```bash
python setup.py bumpversion
```

## publish pypi

```bash
python setup.py publish
```






