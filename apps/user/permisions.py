from django.shortcuts import redirect, render
from django.http.response import Http404, HttpResponse
from django.contrib.auth.mixins import AccessMixin


class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('custom_login')

        if self.request.user.role == 'director':
            if request.path != '/':
                raise Http404
            return super().dispatch(request, *args, **kwargs)

        elif self.request.user.role == 'shop':
            if request.path != '/shop/':
                raise Http404
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404