# -*- coding: utf-8 -*-
from rest_framework import serializers


def serializer_factory(_name, **kwargs):
    ser_cls = type(_name, (serializers.Serializer,), kwargs)
    return ser_cls
