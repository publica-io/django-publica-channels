# -*- coding: utf-8 -*-
import logging
import re

from django.core.exceptions import MiddlewareNotUsed

from .models import Resolution
from .settings import USE_CHANNELS


logger = logging.getLogger(__name__)


class ChannelResolutionMiddleware(object):
    '''Given a request, resolve the Channel.'''

    def __init__(self):
        '''
        This middleware must be enabled, as well as included in
        MIDDLEWARE_CLASSES

        '''

        if not USE_CHANNELS:
            logger.debug(
                'CHANNELS_USE_CHANNELS setting must be True to use this '
                'middleware.'
            )
            raise MiddlewareNotUsed

    def process_request(self, request):
        logger.debug('ChannelResolutionMiddleware.process_request entered')
        request.channel = None

        try:
            http_host = request.META['HTTP_HOST']
        except KeyError:
            logger.error('No Host header in request, cannot resolve Channel')
            return None

        ###
        # TODO, the algorithm for resolving to a single Channel is TBD.
        ###

        # 0. “wildcard” domain matching, blarg O(N) for Resolution
        # domains starting with ‘.’. FIXME not terribly efficient.
        for wild_res in Resolution.objects.filter(domain__startswith='.',
                                                  uripattern=''):
            if http_host.endswith(wild_res.domain):
                logger.debug(
                    'Wildcard host-only Resolution: {}'.format(wild_res)
                )
                logger.debug('Channel is {}'.format(wild_res.channel))
                request.channel = wild_res.channel
                request.META['CHANNEL_SLUG'] = request.channel.slug
                return None

        # 1. Hostname–only Channel Resolution
        try:
            hostonly_res = Resolution.objects.filter(
                domain__endswith=http_host,
                uripattern=''
            )[0]
            logger.debug('Host-only Resolution: {}'.format(hostonly_res))
            logger.debug('Channel is {}'.format(hostonly_res.channel))
            request.channel = hostonly_res.channel
            request.META['CHANNEL_SLUG'] = request.channel.slug

            return None

        except IndexError:
            logger.debug(
                'No hostname-only Resolution for {}'.format(http_host)
            )

        # 2. URI path regex testing, first to match wins
        simple_res = Resolution.objects.filter(domain__endswith=http_host,
                                               uripattern__isnull=False)
        logger.debug('URI Resolutions: {}'.format(simple_res))

        for res in simple_res:
            logger.debug(
                'Resolution: {} URI Pattern: {}'.format(res, res.uripattern)
            )

            if re.match(res.uripattern, request.path):
                logger.debug('Channel is {}'.format(res.channel))
                request.channel = res.channel
                request.META['CHANNEL_SLUG'] = request.channel.slug

                return None

        return None

    # will other methods be useful? process_view,
    # process_template_response, process_response, process_exception
