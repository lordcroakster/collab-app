from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "Invalid method"
        }, status=405)
    
    try:
        body=json.loads(request.body)
        username=body["username"]
        password=body["password"]
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Bad JSON provided/missing fields"
        }, status=400)
    except KeyError:
        return JsonResponse({
            "error": "Username and password are required"
        }, status=400)

    user=authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({
            "error": "Login details incorrect"
        }, status=401)

    login(request, user)

    return JsonResponse({
        "message": "Successfully loggin in",
        "username": user.username
    }, status=200)

@csrf_exempt
def logout_view(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "Method not allowed"
        },status=405)

    user=request.user

    if not user.is_authenticated:
        return JsonResponse({
            "error": "You are not logged in."
        },status=400)

    logout(request)

    return JsonResponse({
        "message": "Successfully logged out"
    },status=200)

@csrf_exempt
def render_login(request):
    return render(request, "accounts/login.html")