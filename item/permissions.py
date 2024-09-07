from rest_framework.permissions import BasePermission
from . models import Menu
from app_user.models import Employee


# custom permissions to allow restaurant owner or employees to manage the menu
class CanAdd(BasePermission): 
      def has_permission(self, request, view):
            # authenticated check
            if not request.user.is_authenticated:
                  return False
      
            # checking owner
            if getattr(request.user, 'profile', None) and request.user.profile.role == 'owner':
                  return True
            
            # check for manager
            try:
                  employee = Employee.objects.get(user = request.user)
                  if employee.restaurant:
                        return True
                  return False
            except Employee.DoesNotExist:
                  return False
      
class CanManage(BasePermission):
      def has_object_permission(self, request, view, obj):
            if not request.user.is_authenticated:
                  return False
            
            # check the creator of the menu
            if obj.user == request.user:
                  return True
            
            # if the user is an employee under the owner
            try:
                  employee = Employee.objects.get(user=request.user, owner__user = obj.user)
                  return True
            except Employee.DoesNotExist:
                  return False