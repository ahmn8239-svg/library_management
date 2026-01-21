def is_manager(request):
    """
    Context processor to check if the user is a manager or admin.
    Safely handles cases where user has no employee profile.
    """
    user = request.user
    if not user.is_authenticated:
        return {'is_manager': False}
    
    
    if user.is_superuser:
        return {'is_manager': True}
    
    # Use select_related if possible or check attribute directly
    # Check if the role is 'manager' without triggering multiple queries
    employee = getattr(user, 'employee', None)
    if employee and employee.role == 'manager':
        return {'is_manager': True}
        
    return {'is_manager': False}
