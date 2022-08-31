import uuid
from django.db import models
from django.utils import timezone

from rooms.settings import EVENT_TYPES


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')

    class Meta:
        abstract = True


class Room(BaseModel):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=1)


class Event(BaseModel):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    event_type = models.CharField(choices=EVENT_TYPES, default='PUBLIC', max_length=20)
    event_date = models.DateField(default=timezone.now)


class Reservation(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
