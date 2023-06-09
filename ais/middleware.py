from django.shortcuts import redirect
from django.urls import reverse

class StaffMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_staff:
            return redirect(reverse('not_allowed'))  # Замените 'not_allowed' на имя вашего URL-шаблона
        return self.get_response(request)