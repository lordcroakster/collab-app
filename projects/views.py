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

