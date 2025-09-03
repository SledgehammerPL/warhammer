from .models import *

def list_of_shops(request):
    return {
            'list_of_shops' : Shop.objects.all()
    }

