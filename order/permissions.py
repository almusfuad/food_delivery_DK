from rest_framework.permissions import BasePermission



class CanOrder(BasePermission):
      def has_permission(self, request, view):
            user = request.user
            
            if not user.is_authenticated:
                  return False
            
            # with hasattr checks whether the user has relation with profile
            if hasattr(user, 'profile') and user.profile.role == 'customer':
                  return True
            
            return False