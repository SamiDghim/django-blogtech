from django.db import models

# Create your models here.

# Room table

class Room(models.Model):
  # host =
  # topic =
  name = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True) # null : can save room with empty description / blank : can save form with description empty 
  # participants
  updated = models.DateTimeField(auto_now=True) # take snapchot every time we save the room
  created = models.DateTimeField(auto_now_add=True) # take snapchot when we first save/create room

  # string representation of the room
  def __str__(self) -> str:
    return self.name