from django.db import models


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    std_class = models.CharField(max_length=50, blank=False)  # Class
    stream = models.CharField(max_length=150, blank=False)  # Stream
    student_number = models.CharField(max_length=100)  # Stdnt_Id
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
