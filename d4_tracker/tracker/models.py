from django.db import models

class Session(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    activity_type = models.CharField(
        max_length=50,
        choices=[('Helltide', 'Helltide'), ('Dungeon', 'Dungeon'), ('World Boss', 'World Boss')]
    )
    mythics_dropped = models.IntegerField(default=0)
    intelligence = models.IntegerField()  # e.g., 800
    crit_chance = models.FloatField()  # e.g., 0.35 for 35%
    crit_damage = models.FloatField()  # e.g., 1.5 for 150%
    attack_speed = models.FloatField()  # e.g., 1.2 for 20% boost
    lightning_damage = models.FloatField()  # e.g., 20 for 20%
    skill_ranks = models.IntegerField()  # e.g., Ball Lightning rank 5
    paragon_points = models.IntegerField()
    fun_score = models.IntegerField()  # 1-10
    session_length = models.FloatField()  # in minutes
    estimated_dps = models.FloatField(null=True, blank=True)  # Calculated post-save

    def __str__(self):
        return f"{self.date} - {self.activity_type}"