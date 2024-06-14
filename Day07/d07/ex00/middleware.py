from django.utils.deprecation import MiddlewareMixin
from .forms import LoginForm

class LoginFormMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            response.context_data['login_form'] = LoginForm()
        return response