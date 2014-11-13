# -*- coding: utf-8 -*-
from django.conf import settings


USE_CHANNELS = getattr(settings, "CHANNELS_USE_CHANNELS", True)
