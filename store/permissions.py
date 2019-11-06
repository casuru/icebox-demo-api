from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):


    def has_permission(self, request, view):
        
        return request.method == 'GET' or request.user.is_staff or request.user.is_superuser

    
    def has_object_permission(self, request, view, instance):

        return request.method == 'GET' or request.user.is_staff or request.user.is_superuser


