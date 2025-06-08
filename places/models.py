from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('cafe', 'Кафе'),
        ('restaurant', 'Ресторан'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='places/', blank=True, null=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )  # Новое поле для категории
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        return self.reviews.all().aggregate(Avg('rating'))['rating__avg'] or 0

class Review(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.place.title}"

