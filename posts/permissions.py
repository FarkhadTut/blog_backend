from rest_framework.permissions import BasePermission, SAFE_METHODS

class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            if request.method in SAFE_METHODS:
                return True
            else:
                return False
        return super().has_permission(request, view)
    

    def has_object_permission(self, request, view, obj):
        # if request.method in ["DELETE", "PUT", "PATCH"]:
        #     if request.user == obj.author:
        return super().has_object_permission(request, view, obj)
    


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method not in SAFE_METHODS:
                if request.user.is_staff:
                    return True
                return False
            else:
                return True
        else:
            if request.method in SAFE_METHODS:
                return True
            else:
                return False
        return super().has_permission(request, view)
    

    def has_object_permission(self, request, view, obj):
        if request.method in ["DELETE", "PUT", "PATCH"]:
            if not request.user.is_staff:
                if request.user == obj.author:
                    return True
                else:
                    return False
            else:
                return True
        return super().has_object_permission(request, view, obj)