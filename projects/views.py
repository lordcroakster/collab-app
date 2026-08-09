from django.shortcuts import render
from django.http import JsonResponse
from .models import Project
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def project_list(request):
    projects=Project.objects.all()
    data=[]

    for project in projects:
        data.append({
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def project_detail(request, project_id):
    if request.method != "GET" and request.method != "DELETE" and request.method != "PUT":
        return JsonResponse({
            "error": "Method not allowed"
        }, status=405)
    
    try:
        project=Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return JsonResponse({
                "erorr": "Data does not exist"
            }, status=404)

    if request.method == "GET":
        return JsonResponse({
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at
        }
            )

    if request.method == "DELETE":
        project.delete()
        return JsonResponse({
            "message": "Project delete"
        }, status=200)

    if request.method == "PUT":
        try:
            body=json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid json"
            }, status=400)
       
        try:
            project.name=body["name"]
            project.description=body["description"]
            if project.name == "":
                return JsonResponse({
                    "error": "a project name is required"
                },status=400)
            project.save()

            return JsonResponse({
                "message": "Updated",
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at,
            }, status=200)
        except KeyError:
            return JsonResponse({
                "message": "fields missing"
            }, status=400)



@csrf_exempt
def project_create(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "error": "method not allowed"
            }, status=405
        )
    
    body=json.loads(request.body)
    project=Project.objects.create(
        name=body["name"],
        description=body["description"],
    )

    return JsonResponse({
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_at": project.created_at
        },
        status=201,
    )

