from django import forms
from .models import Session

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = [
            'activity_type', 'mythics_dropped', 'intelligence', 'crit_chance',
            'crit_damage', 'attack_speed', 'lightning_damage', 'skill_ranks',
            'paragon_points', 'fun_score', 'session_length'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add padding and alignment with Tailwind classes
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'p-1 mb-1 rounded bg-gray-800 text-white border border-gray-600 focus:border-green-500',
                'placeholder': field.label  # Use label as placeholder for clarity
            })