from rest_framework.permissions import BasePermission
from . models import Menu
from app_user.models import Employee, Restaurant


# custom permissions to allow restaurant owner or employees to manage the menu
class CanAccess(BasePermission): 
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
      def has_permission(self, request, view):
            user = request.user
            
            if request.method in ['POST', 'PUT', 'PATCH']:
                  if user.profile.role =='owner':
                        return True
                  elif hasattr(user, 'employee') and user.employee.isManager:
                        return True
                  return False
            
            # Allow get permissions
            return True