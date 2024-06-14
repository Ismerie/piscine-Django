from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import LoginForm
from django.views.generic import View
from django.shortcuts import render
from time import time
from django.contrib.auth import logout as auth_logout
from django.middleware.csrf import get_token
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_protect


class LoginView(FormView):
    template_name = "account/account.html"
    form_class = LoginForm
    success_url = reverse_lazy('login')
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            if self.request.user.is_authenticated:
                return JsonResponse({"message": "USER ALREADY LOGGED IN"},
                                    status=400)
            return JsonResponse({"message": "ajax call"}, status=201)
        else:
            return super().get(request, *args, **kwargs)


    def form_valid(self, form):
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            usrname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            user = authenticate(self.request,
                                username=usrname,
                                password=pwd)
            if user is None:
                return JsonResponse({"message": "invalid credentials"},
                                    status=400)
            login(self.request, user)
            return JsonResponse({"message": "success"}, status=200)

    def form_invalid(self, form):
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({"message": f"error invalid form {form.errors}"},
                                status=400)
        else:
            return super().form_invalid(form)



def logout(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = {
                'message': 'success',
            }
            try:
                auth_logout(request)
                return JsonResponse(data, status=200)
            except Exception as e:
                print("logout error : ", e)
                return JsonResponse({'error': f"error unable to log out : {e}"},
                                    status=401)
        else:
            return JsonResponse({'error': 'user not log'}, status=401)

def getUsername(request):
    if request.user.is_authenticated:
        user_details = {
            'username': request.user.username,
        }
        return JsonResponse(user_details)
    else:
        return JsonResponse({'error': 'user not log'}, status=401)

@require_GET
@csrf_protect
def updateCSRFToken(request):
    new_token = get_token(request)
    return JsonResponse({'newToken': new_token})