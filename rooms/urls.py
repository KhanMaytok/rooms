from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from core.urls import router
from core.views import AuthUserAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="ROOMS AND EVENTS API",
        default_version='v1',
        description="Test",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sakya_stelios@hotmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', AuthUserAPIView.as_view(), name='login'),
    path('', include(router.urls)),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
