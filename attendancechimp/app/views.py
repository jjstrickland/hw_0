"""
views.py — HTTP request handlers for AttendanceChimp.

Each view corresponds to one URL endpoint.  Views receive an HTTP request,
interact with the database via models.py, and return an HTTP response.
"""

from django.shortcuts import render, redirect
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseBadRequest, JsonResponse)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import io

from .models import StudentProfile, InstructorProfile
# from .models import (InstructorProfile, StudentProfile, Course, Enrollment,
#                      Lecture, QRCodeUpload, is_instructor, is_student,
#                      getUploadsForCourse)

CDT = ZoneInfo("America/Chicago")


# ---------------------------------------------------------------------------
# HW2  — index, time, sum
# ---------------------------------------------------------------------------

def time_view(request):
    """A view function that returns a plain text HttpResponse containing
        the current Central time formatted as 'HH:MM'"""
    current_time = datetime.now(CDT)
    formatted_time = current_time.strftime("%H:%M")
    return HttpResponse(formatted_time)

def sum_view(request):
    """A view that reads query parameters n1 and n2 from the GET request, 
    converts them to a number, and returns a HTTP response of the form 
    {"sum": value}, where value is a number."""
    n1 = float(request.GET.get('n1', 0))
    n2 = float(request.GET.get('n2', 0))
    result = n1 + n2
    return HttpResponse(f"<p>{result:g}</p>", content_type="text/html")

# ---------------------------------------------------------------------------
# HW4  — user creation
# ---------------------------------------------------------------------------

def index(request):
    """Render the home page (index.html)."""

    current_time = datetime.now(CDT).strftime("%H:%M")

    context = {
        "current_time": current_time,
        "current_user": request.user,
    }
    return render(request, 'app/index.html', context)


def new(request):
    """Display the sign-up form. Only GET requests are allowed."""

    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)

    return render(request, "app/new.html")


@csrf_exempt
def createUser(request):
    """Create a new user and their student or instructor profile."""

    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    email = request.POST.get("email")
    user_name = request.POST.get("user_name")
    password = request.POST.get("password")
    is_student = request.POST.get("is_student")

    if not email or not user_name or not password:
        return HttpResponse("Missing required information", status=400)

    if is_student not in ["1", "0"]:
        return HttpResponse("Invalid account type", status=400)

    if User.objects.filter(email=email).exists():
        return HttpResponse("Email already exists", status=400)

    user = User.objects.create_user(
        username=user_name,
        email=email,
        password=password)

    if is_student == "1":
        StudentProfile.objects.create(student_name=user_name)
    else:
        InstructorProfile.objects.create(instructor_name=user_name)

    login(request, user)

    return HttpResponse("User created successfully", status=200)


def logout_view(request):
    """Logout the current user."""

    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    logout(request)
    return redirect("/app/")


# ---------------------------------------------------------------------------
# HW5  — courses, lectures, QR uploads, dump
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# HW6  — getUploads
# ---------------------------------------------------------------------------



