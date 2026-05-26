from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.team_tasks, name='team_tasks'),
    path('take/<int:task_id>/', views.take_task, name='take_task'),
    path('update/<int:task_id>/', views.update_status, name='update_status'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),

]
