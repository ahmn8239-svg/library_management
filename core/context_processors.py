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
    
    
    if hasattr(user, 'employee') and user.employee.role == 'manager':
        return {'is_manager': True}
        
    return {'is_manager': False}
