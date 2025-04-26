from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Board
from .forms import BoardForm
from django.shortcuts import get_object_or_404


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

# Create Board
@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect('dashboard')
    else:
        form = BoardForm()
    return render(request, 'boards/board_form.html', {'form': form, 'title': 'Create Board'})

# Update Board
@login_required
def edit_board(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BoardForm(instance=board)
    return render(request, 'boards/board_form.html', {'form': form, 'title': 'Edit Board'})

# Delete Board
@login_required
def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    if request.method == 'POST':
        board.delete()
        return redirect('dashboard')
    return render(request, 'boards/confirm_delete.html', {'board': board})
