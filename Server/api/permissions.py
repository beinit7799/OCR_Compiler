from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

class IsSnippetOwner(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user