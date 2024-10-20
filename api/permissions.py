from rest_framework import permissions
from rest_framework.authtoken.models import Token

class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request,view, obj):
        return obj.author == request.user
    
class HasApiToken(permissions.BasePermission):

    def has_permission(self, request, view):
        return Token.objects.filter(user=request.user.id).exists()