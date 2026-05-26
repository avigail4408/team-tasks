from django.db import models
from django.contrib.auth.models import User
from team_tasks import settings


class StatusTasks(models.TextChoices):
    NEW = 'NEW', 'חדש'
    IN_PROGRESS = 'IN_PROGRESS', 'בתהליך'
    COMPLETED = 'COMPLETED', 'הושלם'

class StatusUser(models.TextChoices):
    ADMIN='ADMIN','מנהל'
    WORKER='WORKER','עובד'
class Team(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}'


class Worker(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name=models.CharField(max_length=100)
    status=models.CharField(
        max_length=20,
        choices=StatusUser.choices,
        default=StatusUser.WORKER
    )
    team=models.ForeignKey(Team, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return f'{self.name} {self.status} {self.team}'


class Task(models.Model):
    name = models.CharField(max_length=100)
    description =models.CharField(max_length=100)
    dateEndTask=models.DateField()
    status = models.CharField(
        max_length=20,
        choices=StatusTasks.choices,
        default=StatusTasks.NEW
    )
    worker = models.ForeignKey(Worker, null=True, blank=True, on_delete=models.SET_NULL)
    team=models.ForeignKey(Team, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return f'{self.name} {self.description} {self.dateEndTask} {self.status} {self.team}'






# Create your models here.
