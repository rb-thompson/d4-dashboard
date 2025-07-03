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
        self.fields['activity_type'].help_text = ''
        for field_name, field in self.fields.items():
            field.help_text = ''  # Clears all help text
        # Define activity type as a ChoiceField with dropdown
        self.fields['activity_type'] = forms.ChoiceField(
            choices=[
                ('', 'Select Activity'),
                ('helltide', 'Helltide'),
                ('nightmare_dungeon', 'Nightmare Dungeon'),
                ('world_boss', 'World Boss'),
                ('seasonal_realm', 'Seasonal Realm'),
                ('pit_of_artificers', 'Pit of the Artificers')
            ],
            widget=forms.Select(attrs={'class': 'p-1 mb-1 rounded bg-gray-800 text-white border border-gray-600 focus:border-green-500'})
        )
        # Customize placeholders with examples and tooltips
        field_configs = {
            'mythics_dropped': {'placeholder': 'e.g., 2', 'title': 'Number of Mythics dropped'},
            'intelligence': {'placeholder': 'e.g., 500', 'title': 'Intelligence stat'},
            'crit_chance': {'placeholder': 'e.g., 25.5', 'title': 'Critical hit chance (%)'},
            'crit_damage': {'placeholder': 'e.g., 150', 'title': 'Critical damage bonus (%)'},
            'attack_speed': {'placeholder': 'e.g., 1.2', 'title': 'Attacks per second'},
            'lightning_damage': {'placeholder': 'e.g., 200', 'title': 'Lightning damage bonus'},
            'skill_ranks': {'placeholder': 'e.g., 10', 'title': 'Total rank of Lightning skills'},
            'paragon_points': {'placeholder': 'e.g., 150', 'title': 'Current Paragon level'},
            'fun_score': {'placeholder': 'e.g., 7', 'title': 'Fun rating (1-10)'},
            'session_length': {'placeholder': 'e.g., 30', 'title': 'Duration in minutes'}
        }
        for field_name, field in self.fields.items():
            if field_name != 'activity_type':  # Skip activity_type, handled above
                config = field_configs.get(field_name, {})
                field.widget.attrs.update({
                    'class': 'p-1 mb-1 rounded bg-gray-800 text-white border border-gray-600 focus:border-green-500',
                    'placeholder': config.get('placeholder', ''),
                    'title': config.get('title', '')
                })