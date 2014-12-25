"""
player/view/logout.py
"""
from django.views import generic
from django.core.urlresolvers import reverse_lazy


class Do(generic.RedirectView):
    """ Blindly log out any request that hits this url with a GET """
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(self.request, 'You have logged out!')
        return super(LogoutView, self).get(request, *args, **kwargs)
