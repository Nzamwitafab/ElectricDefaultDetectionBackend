from .views import (
    register_user_view,
    login_user_view,
    get_user_by_id_view,
    get_all_users_view,
    update_user_view,
    delete_user_view
)
from django.urls import path
from django.http import HttpResponse

print("==== CORE URLS LOADED ====")

def direct_response(request):
    return HttpResponse("DIRECT RESPONSE WORKS")

urlpatterns = [
    path('test-direct/', direct_response),  # Test endpoint
    path('login/', login_user_view, name='login_user_view'),
    path('register/', register_user_view, name='register_user_view'),
    path('users/', get_all_users_view, name='get_all_users_view'),
    path('users/<int:user_id>/', get_user_by_id_view, name='get_user_by_id_view'),
    path('users/<int:user_id>/update/', update_user_view, name='update_user_view'),
    path('users/<int:user_id>/delete/', delete_user_view, name='delete_user_view'),
]
