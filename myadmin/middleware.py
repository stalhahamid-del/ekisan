from django.shortcuts import render,redirect
from django.utils.deprecation import MiddlewareMixin

class AuthMiddlewareAdmin(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = ['/admin/', '/admin/logout/']  
        user_id = request.session.get('admin_id')
        if user_id and request.path == '/admin/':
            return redirect('/admin/home/')
        if not user_id and request.path.startswith('/admin/') and request.path not in excluded_paths:
            return redirect('/admin/')
        return None

