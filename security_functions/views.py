from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

@ensure_csrf_cookie
def tokenView(request):
    return JsonResponse({'csrf_token': get_token(request)})