from rest_framework import permissions


        
        

class IsSearcher(permissions.BasePermission):
    message = "You do not have permission to perform searching"
    def has_permission(self, request, view):
        return bool(request.user and request.user.role=="search")
class IsCreator(permissions.BasePermission):
    message = "You do not have permission to perform creating"
    def has_permission(self, request, view):
        return bool(request.user and request.user.role=="create")