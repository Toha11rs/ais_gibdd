from django.shortcuts import redirect


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, что текущий пользователь авторизован
        if not request.user.is_authenticated:
            # Если пользователь не авторизован, перенаправляем его на страницу входа
            return redirect('entryEmployee')

        response = self.get_response(request)
        return response
