from django import forms
from .models import Board, Event, Tag

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description', 'location', 'start_date', 'end_date']

class EventForm(forms.ModelForm):
    new_tag = forms.CharField(required=False, help_text="New tag name (optional).")
    new_tag_color = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'color'}),
        initial="#CCCCCC",
        help_text="Pick a color for the new tag (optional)."
    )

    class Meta:
        model = Event
        fields = ['title', 'start_time', 'end_time', 'description', 'tags']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'tags': forms.Select,
        }

    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board', None)
        super().__init__(*args, **kwargs)
        if board:
            self.fields['tags'].queryset = board.tags.all()
        self.board = board

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'})
        }