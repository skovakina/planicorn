from django import forms
from .models import Board
from .models import Event

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', 'location', 'start_date', 'end_date']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_time', 'end_time', 'description', 'tags']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'tags': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board', None)
        super().__init__(*args, **kwargs)
        if board:
            self.fields['tags'].queryset = board.tags.all()