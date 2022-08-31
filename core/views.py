from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from core import serializers
from core.models import Event, Room, Reservation
from core.serializers import LoginSerializer, ReserveCreatedSerializer, ReserveSerializer, \
    ReserveDeleteConfirmedSerializer, ReserveDeleteSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update']:
            return (IsAuthenticated(),)
        return (AllowAny(),)

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            queryset = Event.objects.all()
        else:
            queryset = Event.objects.filter(event_type='PUBLIC')
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # check if the room is available for this date
        data = serializer.validated_data
        is_scheduled = Event.objects.filter(room_id=data.get('room'), event_date=data.get('event_date'))

        if is_scheduled.count():
            raise NotFound(detail='Room is already reserved')

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(operation_description="Booking a place for the event",
                         responses={200: ReserveCreatedSerializer()}, request_body=ReserveSerializer)
    @action(detail=True, methods=['post'], url_path='customer/reservation')
    def create_reservation(self, request, pk=None):
        event = self.get_object()
        # check if eventroom is public and has any available space
        if event.event_type != 'PUBLIC':
            raise NotFound(detail='Event is private')

        # count bookings
        bookings = Reservation.objects.filter(event=event).count()
        if bookings >= event.room.capacity:
            raise NotFound(detail='Room for this event is a full capacity')
        reservation = Reservation.objects.create(event=event)
        return Response({'reservation': reservation.id, 'room': event.room.name})

    @swagger_auto_schema(operation_description="Delete a booking for the event",
                         responses={200: ReserveDeleteConfirmedSerializer()}, request_body=ReserveDeleteSerializer)
    @action(detail=True, methods=['post'], url_path='customer/reservation/delete')
    def delete_reservation(self, request, pk=None):
        event = self.get_object()
        reservation = get_object_or_404(Reservation, pk=request.data.get('reservation'))
        reservation.delete()
        return Response({'message': f'Your reservation for the event "{event.name}" is deleted'})


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = serializers.RoomSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update']:
            return (IsAuthenticated(),)
        return (AllowAny(),)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # check if room have any events
        events = Event.objects.filter(room=instance)

        if events.count():
            raise NotFound(detail='Room have events in the past/future. Delete is not allowed.')

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthUserAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_description="Returns access and refresh token for an existent user",
                         responses={200: LoginSerializer()}, request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        user = authenticate(username=serializer.initial_data['username'],
                            password=serializer.initial_data['password'])
        if user is None:
            raise NotFound(detail='Usuario o contraseña incorrectos')

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
