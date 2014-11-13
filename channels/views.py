# -*- coding: utf-8 -*-


class ChannelListMixin(object):
    '''
    Override get_queryset to make use of channels if it is installed to
    filter the results

    '''

    def get_queryset(self):
        if hasattr(self.model.objects, 'channel'):
            return self.model.objects.channel(self.request.channel)
        else:
            return super(ChannelListMixin, self).get_queryset()


class ChannelDetailMixin(object):
    '''
    Override get_queryset to make use of channels if it is installed to
    filter the results

    '''

    def get_queryset(self):
        slug = self.kwargs.get('slug')

        if hasattr(self.model.objects, 'channel') and slug:
            return self.model.objects.channel(self.request.channel).filter(
                slug=slug
            )
        else:
            return super(ChannelDetailMixin, self).get_queryset()
