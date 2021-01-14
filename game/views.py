from django.shortcuts import render

# Create your views here.
def create_character(request):
    if request.method == 'POST':
        form = NewCharacterForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = NewCharacterForm()
    context = {
        'form': form
    }
    return render (request,'game/newcharacter.html', context)
