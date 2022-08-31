from core import views

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'event', views.EventViewSet)
router.register(r'room', views.RoomViewSet)
