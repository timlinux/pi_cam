# coding=utf-8
"""Urls for changelog application."""

from django.conf.urls import url
from views import index

urlpatterns = [
    url(r'^$', index, name='index')
]

