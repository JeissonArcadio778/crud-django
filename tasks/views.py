from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskCreateForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':

        return render(request, 'signup.html', {
            "form": UserCreationForm
        })

    else:

        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except:
                return render(request, 'signup.html', {
                    "form": UserCreationForm,
                    "error": 'User already exists'
                })
        return render(request, 'signup.html', {
            "form": UserCreationForm,
            "error": 'Password does not match'
        })


@login_required
def signout(request):

    logout(request)

    return redirect('home')


def signin(request):

    if request.method == 'GET':

        return render(request, 'login.html', {
            "form": AuthenticationForm
        })

    else:

        try:

            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])

            if user is None:
                return render(request, 'login.html', {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect"
                })
            else:
                login(request, user)  # save session
                return redirect('tasks')
        except:

            return render(request, 'login.html', {
                "form": AuthenticationForm,
                "error": "Error in login"
            })

@login_required
def tasks(request):

    # listar las que no estan completadas
    tasks = Task.objects.filter(user=request.user, completedAt__isnull=True)

    return render(request, 'tasks.html', {
        'status': 'pending',
        'tasks': tasks
    })


@login_required
def task_by_id(request, task_id):

    try:

        if request.method == 'GET':
            task = Task.objects.get(pk=task_id)
            form = TaskCreateForm(instance=task)
            return render(request, 'task_by_id.html', {
                'task': task,
                'form': form
            })
        else:
            task = Task.objects.get(pk=task_id, user = request.user)
            form = TaskCreateForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')

    except:

        return render(request, 'task_by_id.html', {
            'error': 'Task does not exist'
        })


@login_required
def complete_task(request, task_id):

    task = get_object_or_404(Task, pk = task_id, user = request.user)

    if request.method == 'POST':
        task.completedAt = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required

def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            "form": TaskCreateForm
        })
    else:

        try:
            form = TaskCreateForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except Exception as error:
            print(error)
            return render(request, 'create_task.html', {
                "form": TaskCreateForm,
                "error": "Error in create task. Please send valid data"
            })

@login_required
def tasks_completed(request):
    # listar las que no estan completadas
    tasks_completed = Task.objects.filter(user=request.user, completedAt__isnull=False).order_by('-completedAt')

    return render(request, 'tasks.html', {
        'status': 'Completed',
        'tasks': tasks_completed
    })

