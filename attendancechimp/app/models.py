"""
models.py — Data model for AttendanceChimp.

AttendanceChimp is an electronic class attendance tool.  Instructors create
courses and lectures; each lecture is assigned a random QR code.  Students
photograph the QR code and upload the image.  The system decodes the QR code,
matches it to a lecture, and records the attendance.

Entities
--------
- CourseProfile   : extends Django User → instructor-specific data
- StudentProfile  : extends Django User → student-specific data
- Course          : a course taught by one instructor
- Enrollment      : junction table linking students to courses
- Lecture         : a single class meeting (has a QR-code identifier)
- QRCodeUpload    : a student's uploaded QR-code photograph
"""

from django.db import models
from django.contrib.auth.models import User

import logging
import string
import random

logger = logging.getLogger(__name__) # set up tracking, auditing, and debugging
                                                               # allows using logger.warning(), logger.error(), 
                                                               # logger.info(), etc. Better than print() for debuggin... 


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

class InstructorProfile(models.Model):
    """ Stores information about each instructor
    Attributes:
        instructor_id: Unique identifier for the instructor.
        instructor_name: The instructor's name."""
    instructor_id = models.AutoField(primary_key=True)
    instructor_name = models.CharField(max_length=100)

class StudentProfile(models.Model):
    """ Stores information about each student
    Attributes:
        student_id: Unique identifier for the student.
        student_name: The student's name."""
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100)

# ---------------------------------------------------------------------------
# Course
# ---------------------------------------------------------------------------

class Course(models.Model):
    """ Stores each course offered
    Attributes:
        course_id: Unique identifier for the course.
        course_name: The course's name.
        instructor_id: instructor id from InstructorProfile
        meeting_schedule: schedule the course meets"""
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    instructor_id = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    meeting_schedule = models.CharField(max_length=100)

# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------

class Enrollment(models.Model):
    """ Connects students to courses
    Attributes:
        enrollment_id: Unique identifier for enrollment
        student: student_id from StudentProfile
        course: course_id from Course"""
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

# ---------------------------------------------------------------------------
# Lecture
# ---------------------------------------------------------------------------

class Lecture(models.Model):
    """ Stores individual class meetings
    Attributes:
        lecture_id: Unique identifier for each lecture
        course: course_id from Course
        date: date of lecture
        qr_identifier: unique identifier of each QR code"""
    lecture_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField()
    qr_identifier = models.CharField(max_length=100, unique=True)

# ---------------------------------------------------------------------------
# QR Code Upload
# ---------------------------------------------------------------------------

class QRCodeUpload(models.Model):
    """ Stores a student's QR Code submission
    Attributes:
        qr_id: Unique identifier for each QR code
        student - student_id from StudentProfile
        lecture - lecture_id from Lecture, if uploaded"""
    qr_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.SET_NULL, null=True, blank=True)

# ---------------------------------------------------------------------------
# Helper / API functions
# ---------------------------------------------------------------------------



