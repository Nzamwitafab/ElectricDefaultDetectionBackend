# core/urls.py
from django.urls import path
from .views import register_user_view,login_user_view
from django.http import HttpResponse
print("==== CORE URLS LOADED ====")
def direct_response(request):
    return HttpResponse("DIRECT RESPONSE WORKS")
urlpatterns = [
    path('test-direct/', direct_response),  # Add this
    path('login/', login_user_view, name='login_user_view'),
    path('register/', register_user_view, name='register_user_view'),
]
