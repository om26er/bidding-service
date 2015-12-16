# from rest_framework import permissions
#
#
# class IsOwner(permissions.BasePermission):
#
#     def has_permission(self, request, view, obj=None):
#         return obj is None or obj.from_user == request.user
