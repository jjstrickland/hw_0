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
from django.contrib.auth import authenticate, login
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import io

# from .models import (InstructorProfile, StudentProfile, Course, Enrollment,
#                      Lecture, QRCodeUpload, is_instructor, is_student,
#                      getUploadsForCourse)

CDT = ZoneInfo("America/Chicago")


# ---------------------------------------------------------------------------
# HW2  — index, time, sum
# ---------------------------------------------------------------------------

def index(request):
    """Render the home page (index.html)."""

    context = {}
    return render(request, 'app/index.html', context)

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



# ---------------------------------------------------------------------------
# HW5  — courses, lectures, QR uploads, dump
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# HW6  — getUploads
# ---------------------------------------------------------------------------



