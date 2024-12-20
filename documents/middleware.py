from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is authenticated and is an admin, redirect them to the admin dashboard
        if request.user.is_authenticated and request.user.is_staff:
            if not request.path.startswith('/admin/'):
                return redirect('admin:index')  # Redirect admins to the admin section
        
        # Avoid redirect loop by checking if the current page is the 'index' page
        elif not request.user.is_authenticated and not request.path.startswith('/login/') and not request.path.startswith('/static/') and request.path != '/':
            # If the user is not authenticated and tries to access any page other than login, static assets, or index,
            # we set a session flag for the modal and redirect them to the login view
            request.session['show_login_modal'] = True
            return redirect('index')
        
        return self.get_response(request)