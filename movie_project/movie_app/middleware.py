from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import UserToken


class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if 'HTTP_AUTHORIZATION' in request.META:
        #     token = request.META['HTTP_AUTHORIZATION'].split()[1]
        #     db_token = UserToken.objects.filter(token=token)
        #     if not db_token.exists():
        #         response = HttpResponse("Invalid Token! please log in", content_type="text/plain")
        #         return response
        #     else:
        #         response = self.get_response(request)
        #         return response
        #
        # if request.META.get('PATH_INFO') == '/login/':
        #     if 'user' in request.session:
        #         return redirect('movie_app:index')
        #
        # if request.META.get('PATH_INFO') != '/login/':
        #     if 'user' not in request.session:
        #         return redirect('movie_app:login')

        response = self.get_response(request)
        return response
