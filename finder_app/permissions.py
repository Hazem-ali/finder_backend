from rest_framework import permissions


        
        
class IsSupervisorOrInformerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow delete permissions for the informer
        if request.method == 'DELETE':
            return obj.informer == request.user
        # Allow update permissions only for supervisors
        return bool(request.user and request.user.is_supervisor)