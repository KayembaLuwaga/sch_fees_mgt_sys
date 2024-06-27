# course/models.py
from django.db import models
from django.db.models import Sum


class Course(models.Model):
    name = models.CharField(max_length=100)
    course_desc = models.TextField()
    level = models.CharField(max_length=100)
    total_amount = models.FloatField(null=True, blank=True)  # Allow null and blank for dynamic calculation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     # Calculate total_amount based on related fees
    #     total_amount = self.fee_set.aggregate(total=Sum('amount')).get('total') or 0
    #     self.total_amount = total_amount
    #     super().save(*args, **kwargs)

    def __str__(self):
        # return "%s - %s" % (self.name, self.course_desc)
        return f"{self.name} - {self.course_desc}"


class Fee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    fee_desc = models.TextField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fee_desc} - {self.amount}"
