from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import EmergencyReport, Profile
from django.contrib.auth.models import User   
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password != confirm_password:
            return render(request, "safezone/signup.html", {"error": "Passwords do not match!"})

        if User.objects.filter(username=username).exists():
            return render(request, "safezone/signup.html", {"error": "Username already taken!"})

        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Assign role to profile
        user.profile.role = role
        user.profile.save()

        # Auto login
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Redirect based on role
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'police':
                return redirect('police_dashboard')  # optional
            else:
                return redirect('user_dashboard')

    return render(request, "safezone/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on user type
            if user.is_superuser:   # admin
                return redirect("admin_dashboard")
            else:                   # normal user
                return redirect("user_dashboard")
        else:
            return render(request, "safezone/login.html", {"error": "Invalid credentials"})
    
    return render(request, "safezone/login.html")

@login_required
def user_dashboard(request):
    return render(request, "safezone/user_dashboard.html")

@login_required
def admin_dashboard(request):
    return render(request, "safezone/admin_dashboard.html")

@login_required
def police_dashboard(request):
    return render(request, "safezone/police_dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "safezone/index.html")

def send_emergency(request):
    if request.method == "POST":
        user = request.POST.get("user", "Anonymous")
        report = EmergencyReport.objects.create(user=user, status="Emergency")
        return JsonResponse({"message": "Emergency received", "id": report.id})
    return JsonResponse({"error": "Invalid request"}, status=400)

def resolve_emergency(request, report_id):
    try:
        report = EmergencyReport.objects.get(id=report_id)
        report.status = "Resolved"
        report.save()
        return JsonResponse({"message": "Emergency resolved"})
    except EmergencyReport.DoesNotExist:
        return JsonResponse({"error": "Report not found"}, status=404)

@login_required(login_url='login')
def dashboard_view(request):
    role = request.user.profile.role

    if role == "admin":
        return render(request, 'safezone/dashboard_admin.html')
    elif role == "police":
        return render(request, 'safezone/dashboard_police.html')
    else:
        return render(request, 'safezone/dashboard_user.html')