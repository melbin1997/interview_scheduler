from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

USER_TYPE = (
    ("CANDIDATE", "CANDIDATE"),
    ("INTERVIEWER", "INTERVIEWER")
)

class TimeSlot(models.Model):
    user_type = models.CharField(max_length=100, choices= USER_TYPE)
    user_id = models.PositiveIntegerField()
    date = models.DateField()
    start_time = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    end_time = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)])

    def __str__(self):
        return f'{self.user_type} - {self.user_id} - {self.date} :- {self.start_time} - {self.end_time}'