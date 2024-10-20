from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from users.views import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from profile.views import LoginView, RegisterView
from profile.renderers import UserJSONRenderer


renderer_classes = (UserJSONRenderer,)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('app/', include('application.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('app/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('app/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
