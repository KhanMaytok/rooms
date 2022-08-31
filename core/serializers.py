from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Event, Room


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class ReserveSerializer(serializers.Serializer):
    pass


class ReserveCreatedSerializer(serializers.Serializer):
    reservation = serializers.UUIDField()
    room = serializers.CharField()


class ReserveDeleteSerializer(serializers.Serializer):
    reservation = serializers.UUIDField()


class ReserveDeleteConfirmedSerializer(serializers.Serializer):
    message = serializers.CharField()
