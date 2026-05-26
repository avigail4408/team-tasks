from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),  # tasks.urls צריך להכיל path('', login_view, name='login')
]
