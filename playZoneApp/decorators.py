from django.shortcuts import redirect
from functools import wraps

def login_requerido(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login') 
        return func(request, *args, **kwargs)
    return wrapper
