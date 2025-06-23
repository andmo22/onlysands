from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Beach(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    location = models.CharField(max_length=255, null=True, blank=True)
    suburb = models.CharField(max_length=255, null=True, blank=True)
    beach_type = models.JSONField(default=list)  # list of strings
    rating = models.IntegerField(
        null=True, choices=[(i, i) for i in range(8)]
    )  # Choices 0-7
    return_visit = models.BooleanField(null=False)
    tags = models.JSONField(default=list)  # list of strings
    vibe = models.JSONField(default=list)  # list of strings
    review = models.TextField(null=True, blank=True)
    related_walks = models.JSONField(default=list)  # list of strings
    visited = models.BooleanField(null=False)
    other_names = models.JSONField(default=list)  # list of strings
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)

    class Meta:
        verbose_name_plural = "Beaches"

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse("beach-detail", kwargs={"pk": self.pk})


class BeachImage(models.Model):
    beach = models.ForeignKey(Beach, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="beach_images/")

    def __str__(self):
        return f"Image for {self.beach.name}"
        
class Review(models.Model):
    beach = models.ForeignKey(Beach, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(
        null=False, choices=[(i, i) for i in range(8)]
    )  # Choices 0-7
    text = models.TextField(max_length=3000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    was_edited = models.BooleanField(default=False)

    class Meta:
        unique_together = ('beach', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user} on {self.beach.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    last_confirmation_email_sent_at = models.DateTimeField(null=True, blank=True)
    confirmation_token = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.user.username


User._meta.get_field("email")._unique = True
User._meta.get_field("email").blank = False
User._meta.get_field("email").null = False
