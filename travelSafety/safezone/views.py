from django.shortcuts import render
from django.http import JsonResponse
from .models import EmergencyReport

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
    