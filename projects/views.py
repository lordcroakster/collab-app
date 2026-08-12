from django.shortcuts import render
from django.http import JsonResponse
from .models import Project
from django.contrib.auth.models import User
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
    if request.method not in ["GET", "DELETE", "PATCH"]:
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
            "owner": project.owner.username,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at
        }
            )

    if request.method == "DELETE":
        user=request.user
        if not user.is_authenticated:
            return JsonResponse({
                "error": "User not authenticated"
            },status=401)
        if user != project.owner:
            return JsonResponse({
                "error": "User not authorized"
            },status=403)
        
        project.delete()
        return JsonResponse({
            "message": "Project delete"
        }, status=200)

    if request.method =="PATCH":
        user=request.user
        if not user.is_authenticated:
            return JsonResponse({
                "error": "User not logged in."
            },status=401)
        if user != project.owner:
            return JsonResponse({
                "error": "Permission not granted"
            },status=403)
        try:
            body=json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid json"
            },status=400)

        if "name" in body:
            if body["name"] == "":
                return JsonResponse({
                    "error": "A project name cannot be empty."
                },status=400)
            project.name=body["name"]

            
        if "description" in body:
            project.description=body["description"]

        project.save()
        
        return JsonResponse({
                    "message": "Updated",
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "created_at": project.created_at,
                    }, status=200)

@csrf_exempt
def project_create(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "error": "method not allowed"
            }, status=405
        )

    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "User not authenticated"
        }, status=401)

    try:
        body=json.loads(request.body)
        name=body["name"]
        description=body["description"]
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON"
        }, status=400)
    except KeyError:
        return JsonResponse({
            "error": "Fields are required"
        },status=400)
    
    project=Project.objects.create(
        name=name,
        description=description,
        owner=request.user,
    )
    project.members.add(request.user)

    return JsonResponse({
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_at": project.created_at
        },
        status=201,
    )

@csrf_exempt
def project_members(request, project_id):
    print("PROJECT MEMBERS:", request.method, project_id)
    if request.method not in ["GET", "POST", "DELETE"]:
        return JsonResponse({
            "error": "Method not allowed"
        },status=405)


    try:
        project=Project.objects.get(id=project_id)
        owner=project.owner
    except Project.DoesNotExist:
        return JsonResponse({
            "error": "Project does not exist"
        },status=404)
 
    user=request.user

    if not user.is_authenticated:
        return JsonResponse({
            "error": "Please login."
        },status=401)

    if request.method == "POST":
        if owner != user:
            return JsonResponse({
                "error": "You do not have permission."
            },status=403)
        #check user_id exists and is an actual nunmber
        try:
            body=json.loads(request.body)
            new_member_id=body["user_id"]

            if not isinstance(new_member_id, int):
                return JsonResponse({
                    "error": "Field must be an integer"
                },status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid json"
            },status=400)
        except KeyError:
            return JsonResponse({
                "error": "User id must be provided"
            },status=400)

        #check user exists
        try:
            new_member=User.objects.get(id=new_member_id)
        except User.DoesNotExist:
            return JsonResponse({
                "error": "This user does not exist"
            },status=404)

        #check does not already exist
        if project.members.filter(id=new_member_id).exists():
            return JsonResponse({
                "error": "User already part of project",
                "username": new_member.username
            },status=400)
        
        project.members.add(new_member)
        return JsonResponse({
            "message": "User successfully added to project",
            "username": new_member.username
        })

    #list of project members
    if request.method == "GET":
        return JsonResponse({
            "error": "Method not implemented"
        },status=501)

    if request.method == "DELETE":
        return JsonResponse({
            "error": "Method not implemented"
        },status=501)