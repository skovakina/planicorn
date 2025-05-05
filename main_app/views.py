from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Board, Event, Tag
from .forms import BoardForm, EventForm, TagForm
from django.shortcuts import get_object_or_404
from datetime import timedelta

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


@login_required
def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    events = board.events.all()
    hours = list(range(24))

    for event in events:
        print(f"{event.title}: {event.start_time} → {event.end_time} = {event.duration_in_minutes:.2f} min")


    # Create list of dates between start and end date
    days = []
    if board.start_date and board.end_date:
        current_day = board.start_date
        while current_day <= board.end_date:
            days.append(current_day)
            current_day += timedelta(days=1)

    return render(request, 'boards/board_detail.html', {
        'board': board,
        'events': events,
        'hours': hours,
        'days': days,
    })


# Create Event
@login_required
def create_event(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, board=board)
        if form.is_valid():
            event = form.save(commit=False)
            event.board = board
            event.save()
            form.save_m2m()
            return redirect('board_detail', board_id=board.id)
        else:
            print(form.errors) 
    else:
        form = EventForm(board=board)
    return render(request, 'events/event_form.html', {'form': form, 'board': board, 'title': 'Create Event'})

# Edit Event
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, board__owner=request.user)
    board = event.board
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event, board=board)
        if form.is_valid():
            form.save()
            return redirect('board_detail', board_id=board.id)
    else:
        form = EventForm(instance=event, board=board)
    return render(request, 'events/event_form.html', {'form': form, 'board': board, 'title': 'Edit Event'})

# Delete Event
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, board__owner=request.user)
    board_id = event.board.id
    if request.method == 'POST':
        event.delete()
        return redirect('board_detail', board_id=board_id)
    return render(request, 'events/confirm_delete.html', {'event': event})

@login_required
def create_tag(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.board = board
            tag.save()
            return redirect('board_detail', board_id=board.id)
    else:
        form = TagForm()
    
    return render(request, 'tags/tag_form.html', {'form': form, 'board': board})

@login_required
def delete_tag(request, tag_id):
    if request.method == 'POST':
        tag = get_object_or_404(Tag, id=tag_id, board__owner=request.user)
        board_id = tag.board.id
        tag.delete()
        return redirect('board_detail', board_id=board_id)
    else:
        return redirect('dashboard')  # fallback if someone tries GET
