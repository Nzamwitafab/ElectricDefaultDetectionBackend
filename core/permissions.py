from rest_framework.permissions import BasePermission

class HasValidAccessToken(BasePermission):
    # print("==== HAS VALID ACCESS TOKEN PERMISSION====")
    message = "You must be logged in to register new users"
    
    def has_permission(self, request, view):
        # Only allow if user is authenticated via JWT
        return bool(request.user and request.user.is_authenticated)