from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
  host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
  topic =  models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True) 
  name = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True) # null : can save room with empty description (default value is false) / blank : can save form with description empty (default value is false) 
  participants = models.ManyToManyField(User, related_name='participants', blank=True)
  updated = models.DateTimeField(auto_now=True) # take snapchot every time we save the room
  created = models.DateTimeField(auto_now_add=True) # take snapchot when we first save/create room

  # order rooms fetched from database
  class Meta:
    ordering = ['-updated', '-created'] # the '-': DES , without '-': ASC
  # string representation of the room
  def __str__(self):
    return self.name

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
      return self.name

class Message(models.Model):
  # https://docs.djangoproject.com/en/5.0/ref/contrib/auth/
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE) # one to many relationship / SET_NULL: when parent deleted set ForeignKey to null /
  body = models.TextField()
  updated = models.DateTimeField(auto_now=True) # take snapchot every time we save the room
  created = models.DateTimeField(auto_now_add=True) # take snapchot when we first save/create room

  def __str__(self):
    return self.body[0:50] # limit to 50 character
