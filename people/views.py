from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def logixn_view():
    if request.methd == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return render(request,'game/logout.html', context)
            pass

    context = {
    }

def logout_view():
    logout(request)
    context = {
    }
    return render(request,'game/logout.html', context)
    # Redirect to a success page.
