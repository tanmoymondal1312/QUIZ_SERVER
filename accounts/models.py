from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    level = models.PositiveIntegerField(default=1)
    mcq_completed = models.PositiveIntegerField(default=0)
    mcq_solved = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        """
        Override save to automatically update level based on MCQs.
        """
        if self.mcq_completed > 0:
            accuracy = self.mcq_solved / self.mcq_completed
        else:
            accuracy = 0

        # Weighted formula: more weight to correct answers
        new_level = 1 + int((self.mcq_completed * 0.3 + self.mcq_solved * 0.7) // 10)

        # Update the level before saving
        self.level = new_level

        # Call the original save() method
        super().save(*args, **kwargs)
