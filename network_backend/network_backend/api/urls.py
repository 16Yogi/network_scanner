from django.urls import path
from api.view.registration import RegisterUser
from api.view.login import LoginView
from api.view.logout import LogoutView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from api.view.status import SessionStatus
from api.view.session import SessionCheckView
from .view import scan

# View that sets the CSRF cookie
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF cookie set"})

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('csrf/', get_csrf_token, name='get-csrf-token'),  
    path('status/', SessionStatus.as_view(), name='status'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('session/', SessionCheckView.as_view(), name='session-check'),
    path('scan/', scan.network_scan, name='network-scan'),
]
