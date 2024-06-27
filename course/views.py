# course/views.py
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

from course import models
from . import forms
from course.forms import CreateCourseForm, CreateFeeForm


def index(request):
    courses = models.Course.objects.all()
    return render(request, 'course/index.html', {'courses': courses})


def create(request):
    course = CreateCourseForm()
    fee = CreateFeeForm()
    return render(request, 'course/create.html', {'course': course, 'fee': fee})

def store(request):
    if request.method == 'POST':
        course_form = forms.CreateCourseForm(request.POST)
        # fee_form = forms.CreateFeeForm(request.POST)
        # if course_form.is_valid() and fee_form.is_valid():
        if course_form.is_valid():
            course_form.save()
            # fee_form.save()
            messages.success(request, 'Fees Payment Structure created successfully')
            return redirect('course.index')
            # messages.success(request, 'Fees Charge created successfully')
            # return redirect('course.index')
        else:
            return render(request, 'course/create.html', {'course': course_form, 'fee': fee_form})
    else:
        return redirect('course.create')


def edit(request, cid):
    try:
        course = models.Course.objects.get(id=cid)
        fee = models.Fee.objects.filter(course=course)
        course_form = CreateCourseForm(instance=course)
        fee_form = CreateFeeForm(instance=fee.last())
        return render(request, 'course/edit.html', {
            'course': course_form,
            'fee': fee_form,
            'fees': fee,
            'course_id': cid  # Ensure cid is added to context
        })
    except models.Course.DoesNotExist:
        return redirect('course.index')


def update(request, cid):
    if request.method == 'POST':
        try:
            # Get the course instance
            course = models.Course.objects.get(id=cid)

            # Initialize the form with POST data and the existing course instance
            course_form = CreateCourseForm(request.POST, instance=course)

            # Check if the form is valid
            if course_form.is_valid():
                # Save the updated course instance
                course_form.save()

                # Success message
                messages.success(request, 'Course updated successfully')

                # Redirect to course index
                return redirect('course.index')
            else:
                # Render the edit page with validation errors
                return render(request, 'course/edit.html', {
                    'course': course_form,
                    'course_id': cid  # Pass the cid for URL generation
                })
        except models.Course.DoesNotExist:
            # If the course does not exist, show an error message
            messages.error(request, 'The course you are trying to update does not exist.')
            return redirect('course.index')
    else:
        return redirect('course.index')


def delete(request, cid):
    try:
        course = models.Course.objects.get(id=cid)
        course.delete()
        messages.success(request, 'Course deleted successfully')
        return redirect('course.index')
    except models.Course.DoesNotExist:
        return redirect('course.index')

def get_total_amount(request):
    course_id = request.GET.get('course_id')
    if course_id:
        try:
            course = Course.objects.get(id=course_id)
            return JsonResponse({'total_amount': course.total_amount})
        except Course.DoesNotExist:
            return JsonResponse({'total_amount': 0}, status=404)
    return JsonResponse({'total_amount': 0}, status=400)
