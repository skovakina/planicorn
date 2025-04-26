from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Board

@login_required
def dashboard(request):
    boards = Board.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {'boards': boards})

def landing(request):
    return render(request, 'landing.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
