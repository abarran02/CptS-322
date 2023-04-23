from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.gpx_form_upload, name='upload'),
    path('posts/<int:post_id>/', views.post_detail, name='detail'),
    path('addmeal/', views.add_meal, name='add_meal'),
    path('users/', views.user_index, name='user_index'),
    path('users/<int:user_id>/', views.profile, name='profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
