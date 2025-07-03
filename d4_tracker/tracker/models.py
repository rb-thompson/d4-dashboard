from django.db import models

class Session(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    session_length = models.PositiveIntegerField(help_text="Duration in minutes")
    ACTIVITY_TYPES = [
        ('', 'Select Activity'),
        ('helltide', 'Helltide'),
        ('nightmare_dungeon', 'Nightmare Dungeon'),
        ('world_boss', 'World Boss'),
        ('seasonal_realm', 'Seasonal Realm'),
        ('pit_of_artificers', 'Pit of the Artificers')
    ]
    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_TYPES,
        default='',
        help_text="Select from dropdown"
    )
    mythics_dropped = models.PositiveIntegerField(default=0, help_text="Number of Mythics dropped")
    skill_ranks = models.PositiveIntegerField(help_text="Total rank of Lightning skills")
    intelligence = models.PositiveIntegerField(help_text="Intelligence stat")
    lightning_damage = models.PositiveIntegerField(help_text="Lightning damage bonus")
    attack_speed = models.FloatField(help_text="Attacks per second")
    crit_chance = models.FloatField(help_text="Critical hit chance (%)")
    crit_damage = models.FloatField(help_text="Critical damage bonus (%)")
    paragon_points = models.PositiveIntegerField(help_text="Current Paragon level")
    fun_score = models.PositiveIntegerField(help_text="Fun rating (1-10)")
    estimated_dps = models.FloatField(null=True, blank=True, help_text="Calculated DPS")

    def __str__(self):
        return f"Session {self.id} - {self.activity_type}"