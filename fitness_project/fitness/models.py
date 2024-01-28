from django.db import models
from django.contrib.auth.models import User


class WorkoutPlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions')
    workout_plan = models.ForeignKey(
        WorkoutPlan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.workout_plan.title}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.workout_plan.title} - {self.rating}"

    def save(self, *args, **kwargs):
        workout_plan = self.workout_plan
        total_ratings = Rating.objects.filter(
            workout_plan=workout_plan).count()
        total_rating_sum = Rating.objects.filter(
            workout_plan=workout_plan).aggregate(models.Sum('rating'))['rating__sum']
        workout_plan.average_rating = total_rating_sum / total_ratings
        workout_plan.save()

        super().save(*args, **kwargs)
