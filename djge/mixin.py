"""
djge/mixin.py
"""
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class RequireUser(object):
    """ Require user logged in """
    mixin_messages = False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            if self.mixin_messages:
                messages.warning(request, 'Unable to comply, please log in.')
            return redirect('{}?next={}'.format(reverse('auth'), request.path))
        return super(RequireUser, self).dispatch(request, *args, **kwargs)


class RequireOwner(object):
    """ Require user owns object already """

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            raise Http404
        return super(RequireOwner, self).dispatch(request, *args, **kwargs)
