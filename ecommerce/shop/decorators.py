from django.http import HttpResponse
def admin_required(fun):
    def wrapper(request):
        if not request.user.is_superuser:
            return HttpResponse("Admin User Only")
        else:
            return fun(request)
    return wrapper
