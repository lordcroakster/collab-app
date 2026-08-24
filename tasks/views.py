from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from projects.models import Project
from django.http import JsonResponse
import json


#view all project tasks/create new task
@csrf_exempt
def task_list_create(request, project_id):
    if request.method != "GET" and request.method != "POST":
        return JsonResponse({
                    "error": "Method not allowed"
                }, status=405)

    #check project exists
    try:
        project=Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return JsonResponse({
            "error": "Project does not exist."
        }, status=404)

    #check user is logged in
    user=request.user
    if not user.is_authenticated:
        return JsonResponse({
            "error": "Please login"
        },status=401)

    #check if user is a member
    if not project.members.filter(id=user.id).exists():
        return JsonResponse({
            "error": "You do not have permission to view this project"
        },status=403)


    if request.method == "GET":
        tasks=Task.objects.filter(project_id=project_id)
        
        data=[]
        for task in tasks:
            data.append({
                    "id": task.id,
                    "name": task.name
                })

        return JsonResponse(data, safe=False)

    if request.method == "POST":
        try:
            body=json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid json"
            },status=400)

        if "name" not in body or "description" not in body:
            return JsonResponse({
                "error": "Name and description required"
            },status=400)

        if not isinstance(body["name"], str) or not isinstance (body["description"], str):
            return JsonResponse({
                "error": "Name and description must be strings"
            },status=400)

        if body["name"] == "":
            return JsonResponse({
                "error": "Name field cannot be empty"
            },status=400)

        new_task=Task.objects.create(
            name=body["name"],
            description=body["description"],
            completed=False,
            project=project
        )

        return JsonResponse({
            "message": "Task created",
            "id": new_task.id,
            "name": new_task.name
        }, status=201)

#get informatino about a specific task, delete  a task, edit a task
@csrf_exempt
def task_detail(request, project_id, task_id):
    if request.method not in ("GET", "DELETE", "PATCH"):
        return JsonResponse({
            "error": "Method not allowed"
            }, status=405)

    user=request.user
    if not user.is_authenticated:
        return JsonResponse({
            "error": "Please log in"
        },status=401)


    #check if task exists
    try:
        task=Task.objects.get(id=task_id, project_id=project_id)
    except Task.DoesNotExist:
        return JsonResponse({
            "error": "Task does not belong to this project/project doesn't exist"
        }, status=404)
    
    if not task.project.members.filter(id=user.id).exists():
        return JsonResponse({
            "error": "You are not a member of this project."
        },status=403)


    if request.method == "GET":
        return JsonResponse({
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at,
        },status=200)


    if request.method == "DELETE":
        task.delete()

        return JsonResponse({
            "message": "Task deleted"
        }, status=200)

    if request.method == "PATCH":
        try:
            body=json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSon"
            }, status=400)

        if "name" in body:
            if not isinstance(body["name"], str):
                return JsonResponse({
                    "error": "Name must be a string"
                },status=400)
            if body["name"] == "":
                return JsonResponse({
                    "error": "Task must have a name"
                }, status=400)

            task.name=body["name"]

        if "description" in body:
            if not isinstance(body["description"], str):
                return JsonResponse({
                "error": "Description must be a string"
                },status=400)
            task.description=body["description"]

        if "completed" in body:
            if not isinstance(body["completed"], bool):
                return JsonResponse({
                    "error": "Completed field must contain a boolean"
                }, status=400)
            task.completed=body["completed"]

        task.save()
        return JsonResponse({
            "message": "Updated successfully",
            "task_id": task.id,
            "name": task.name,
            "description": task.description,
            "completed": task.completed
        }, status=200)

@csrf_exempt
def render_task_detail(request, project_id, task_id):
    return render(request,
                  "tasks/task-list.html",
                    {
                        "project_id": project_id,
                        "task_id": task_id
                    }
                  )