from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.user_index, name='user_index'),
    path('users/<int:user_id>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='detail'),
    path('new/run/', views.create_run, name='create_run'),
    path('new/meal/', views.create_meal, name='create_meal'),
    path('new/workout/', views.create_workout, name='create_workout'),
    path('new/swim/', views.create_swim, name='create_swim')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
