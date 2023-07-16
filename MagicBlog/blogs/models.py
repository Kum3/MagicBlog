""" """

#normal imports
import uuid
#structured imports
from django.db import models

# Create your models here.
CATEGORY_CHOICES = [
]

class User(models.Model):
    """
    User class.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    Blog class.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    summary = models.CharField(max_length=200)
    description =  models.TextField()
    image = models.ImageField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Like(models.Model):
    """
    Like class.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    """
    Comment class.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    text = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

