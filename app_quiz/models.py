from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class QuizCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)  # new field
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)




class Quiz(models.Model):
    ANSWER_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    category = models.ForeignKey(
        'QuizCategory',
        on_delete=models.CASCADE,
        related_name='quizzes'
    )

    question = models.TextField()

    optA = models.CharField(max_length=255)
    optB = models.CharField(max_length=255)
    optC = models.CharField(max_length=255)
    optD = models.CharField(max_length=255)

    correct_ans = models.CharField(
        max_length=1,
        choices=ANSWER_CHOICES
    )

    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)

    seen_by = models.ManyToManyField(
        User,
        related_name='seen_quizzes',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']  # ✅ Ensures 1,2,3,4 order when fetching

    def __str__(self):
        return self.question[:50]



class AppUpdate(models.Model):
    link = models.CharField(max_length=1000, unique=True)
    is_update = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link


