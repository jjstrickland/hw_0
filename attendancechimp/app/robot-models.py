
# Part 5 of HW3: Generate models.py using LLM
# LLM Used: ChatGPT
# Prompt given copied below as a docstring:
""" 
I'm working on a project for data engineering class. 
We have setup the basis for an app using django. Here are some instructions for 
a homework assignment this week: 

Draw an Entity Relations (ER) Diagram. 
Your diagram should show all entities, their attributes, and the relationships between them:
• InstructorProfile / StudentProfile tables (instead of one Users table– think why...)
• Course table with at least name, instructor, meeting schedule
• Enrollment table: links students to courses (many-to-many)
• Lecture table: linked to a course, has a date and a QR identifier
• QRCodeUpload table: linked to a student and (optionally) a lecture
Save the diagram as app/docs/my-data-model.png (hand-drawn is permitted if it is clear).
2. Implement the tables from the list above in models.py
Edit attendancechimp/app/models.py and define Django model classes for each table from the ER
diagram (see Django documentation / class slides). Write a detailed doc string and, if applicable,
helper functions.
3. Run Migrations
cd attendancechimp
python manage.py makemigrations app
python manage.py migrate
Both commands must complete without errors.
4. Verify Tables
Use sqlite3 db.sqlite3 ".tables" to confirm your new tables appear alongside the Django
boilerplate tables. here is some information regarding the project: A relational data model organizes data into tables with rows and columns. Relationships be
tween tables are established via foreign keys. Django models are Python classes that the
framework compiles into database tables through a process called migration. This assignment
focuses on what data to store and how to link it, not yet on functionality. 

Here is some more information about the project: 
AttendanceChimp tracks class attendance via QR codes:
• Users: students and instructors (two roles).
• Courses: each has one instructor. Students can enroll in multiple courses.
• Lectures: individual class meetings, each associated with a course.
• QR Code Uploads: photos uploaded by students, each associated with a student and a lecture.
Design requirements: simple to use, supports attendance analytics, robust to cheating.

Please generate an app/models.py that implements creating these 6 classes as specified.
"""

from django.db import models

class InstructorProfile(models.Model):
    """
    Stores the profile information for an instructor.

    Each instructor can teach multiple courses. Separating instructor
    profiles from student profiles allows each role to have its own
    relevant information and relationships.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    """
    Stores the profile information for a student.

    A student can enroll in multiple courses. Student profiles are
    separate from instructor profiles because students and instructors
    have different responsibilities in the attendance system.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Represents a course taught by one instructor.

    Each course has a name, an assigned instructor, and a meeting
    schedule. Students can join courses through the Enrollment model.
    """
    name = models.CharField(max_length=100)
    instructor = models.ForeignKey(
        InstructorProfile,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    meeting_schedule = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    """
    Connects students to courses through a many-to-many relationship.

    Each enrollment links one student to one course. The unique
    constraint prevents the same student from enrolling in the same
    course more than once.
    """
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course_enrollment"
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.course}"


class Lecture(models.Model):
    """
    Represents an individual meeting of a course.

    Each lecture belongs to one course and has a date and a QR
    identifier. The QR identifier can be used to distinguish the
    attendance code for one lecture from those of other lectures.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lectures"
    )
    date = models.DateField()
    qr_identifier = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.course} - {self.date}"


class QRCodeUpload(models.Model):
    """
    Represents a QR code photo uploaded by a student.

    Each upload belongs to one student and can optionally be linked
    to a lecture. Keeping the lecture optional allows an upload to be
    stored even if its intended lecture has not yet been identified.
    """
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="qr_uploads"
    )
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="qr_uploads"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="qr_uploads/")

    def __str__(self):
        return f"QR upload by {self.student} on {self.uploaded_at}"
