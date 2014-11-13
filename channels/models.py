# -*- coding: utf-8 -*-
from django.db import models

from entropy.base import OrderingMixin, SlugMixin, TitleMixin, AttributeMixin


class Channel(TitleMixin, SlugMixin, AttributeMixin):
    # title
    # short_title
    # slug
    # attributes

    pass


class Resolution(OrderingMixin):
    '''
    If Channels are used in a Request / Response context, we can use
    Resolutions to determine which Channel we're dealing with.

    '''

    # order

    channel = models.ForeignKey('Channel')
    domain = models.CharField(max_length=256, blank=True, help_text=(
        'Start with . to match subdomains e.g. .domain.com to match '
        'this.domain.com and www.domain.com'
    ))
    subdomain = models.CharField(max_length=256, blank=True)
    uripattern = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return 'Domain: {}, Order: {}'.format(self.domain, self.order)
