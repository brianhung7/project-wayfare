from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey 

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=150)
    img = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_city = ForeignKey(City, on_delete=models.CASCADE, related_name='profile')
    avatar = models.CharField(max_length=500, default='https://i.imgur.com/eYlOXmc.png')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="post")

    def __str__(self):
        return self.title

    class Meta:
        #If it's not the right direction, remove minus sign
        ordering = ['-created_at'] 