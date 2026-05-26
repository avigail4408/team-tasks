from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Task, Worker, StatusTasks, StatusUser, Team
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
#from django.shortcuts import render, redirect
#from .models import Worker, Team, StatusUser

#from django.contrib.auth import authenticate, login
#from django.shortcuts import render, redirect

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # אם המשתמש לא קיים
        if not User.objects.filter(username=username).exists():
            teams = Team.objects.all()
            return render(request, 'registration/register.html', {
                'teams': teams,
                'statuses': StatusUser.choices,
                'error': 'משתמש לא קיים, רישום נדרש'
            })

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('team_tasks')
        else:
            error = 'סיסמה שגויה'

    return render(request, 'registration/login.html', {'error': error})

def register(request):
    if request.method == 'POST':
        print("--- קיבלתי בקשת רישום! ---")  # זה ידפיס לכם בטרמינל השחור
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        team_id = request.POST.get('team')
        status = request.POST.get('status')

        # יצירת המשתמש ב־Django
        user = User.objects.create_user(username=username, password=password)

        # השגת הצוות שנבחר
        team = Team.objects.get(id=team_id)

        # יצירת Worker המקושר ל־User
        Worker.objects.create(
            user=user,
            name=name,
            status=status,
            team=team
        )

        # התחברות אוטומטית אחרי רישום
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('team_tasks')

    teams = Team.objects.all()
    return render(request, 'registration/register.html', {
        'teams': teams,
        'statuses': StatusUser.choices
    })


@login_required
def take_task(request, task_id):
    worker = get_object_or_404(Worker, user=request.user)
    task = get_object_or_404(Task, id=task_id, team=worker.team)

    if worker.status != StatusUser.WORKER:
        return HttpResponseForbidden()

    if task.worker is None:
        task.worker = worker
        task.status = StatusTasks.IN_PROGRESS
        task.save()

    return redirect('team_tasks')


@login_required
def update_status(request, task_id):
    worker = get_object_or_404(Worker, user=request.user)
    task = get_object_or_404(Task, id=task_id, worker=worker)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in StatusTasks.values:
            task.status = status
            task.save()

    return redirect('team_tasks')
def is_admin(worker):
    return worker.status == StatusUser.ADMIN

@login_required
@user_passes_test(lambda u: is_admin(get_object_or_404(Worker, user=u)))
def add_task(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        date_end = request.POST.get('dateEndTask')
        team_id = request.POST.get('team')
        team = Team.objects.get(id=team_id)
        Task.objects.create(name=name, description=description, dateEndTask=date_end, team=team)
        return redirect('team_tasks')
    teams = Team.objects.all()
    return render(request, 'tasks/add_task.html', {'teams': teams})


@login_required
@user_passes_test(lambda u: is_admin(get_object_or_404(Worker, user=u)))
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.worker:
        return HttpResponseForbidden()  # אסור לערוך אם משויך
    if request.method == 'POST':
        task.name = request.POST.get('name')
        task.description = request.POST.get('description')
        task.dateEndTask = request.POST.get('dateEndTask')
        task.save()
        return redirect('team_tasks')
    return render(request, 'tasks/edit_task.html', {'task': task})


@login_required
@user_passes_test(lambda u: is_admin(get_object_or_404(Worker, user=u)))
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.worker:
        return HttpResponseForbidden()  # אסור למחוק אם משויך
    task.delete()
    return redirect('team_tasks')


@login_required
def team_tasks(request):
    worker = get_object_or_404(Worker, user=request.user)
    tasks = Task.objects.filter(team=worker.team)

    status_filter = request.GET.get('status')
    worker_filter = request.GET.get('worker')

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if worker_filter:
        tasks = tasks.filter(worker_id=worker_filter)

    return render(request, 'tasks/team_tasks.html', {
        'tasks': tasks,
        'worker': worker,
        'status_choices': StatusTasks.choices,  # <-- שולחים את ה־choices

    })
