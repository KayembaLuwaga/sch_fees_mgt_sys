from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from course.models import Course
from enrollment.forms import CreateEnrollForm
from enrollment.models import Enroll


def index(request):
    enrolls = Enroll.objects.all()
    return render(request, 'enrollment/index.html', {'enrolls': enrolls})


def create(request):
    form = CreateEnrollForm()
    return render(request, 'enrollment/create.html', {'form': form})


def get_course_total_amount(request):
    course = Course.objects.get(id=request.POST.get('course_id'))
    return JsonResponse({'data': course.total_amount})


def store(request):
    if request.method == 'POST':
        form = CreateEnrollForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student enrolled successfully')
            return redirect('enroll.index')
        else:
            return render(request, 'enrollment/create.html', {'form': form})
    else:
        return redirect('enroll.index')


def edit(request, eid):
    try:
        enroll = Enroll.objects.get(id=eid)
        form = CreateEnrollForm(instance=enroll)
        return render(request, 'enrollment/edit.html', {'form': form, 'enroll': enroll})
    except Enroll.DoesNotExist:
        return redirect('enroll.index')


def update(request, eid):
    try:
        if request.method == 'POST':
            enroll = Enroll.objects.get(id=eid)
            form = CreateEnrollForm(request.POST, instance=enroll)
            if form.is_valid():
                form.save()
                messages.success(request, 'Enrolled info updated successfully')
                return redirect('enroll.index')
            else:
                return render(request, 'enrollment/edit.html', {'form': form, 'enroll': enroll})
        else:
            return redirect('enroll.index')
    except Enroll.DoesNotExist:
        return redirect('enroll.index')


def delete(request, eid):
    if request.method == 'POST':
        try:
            enroll = Enroll.objects.get(id=eid)
            enroll.delete()
            return redirect('enroll.index')
        except Enroll.DoesNotExist:
            messages.error(request, 'Enrolled info not found')
            return redirect('enroll.index')
    else:
        messages.error(request, 'Invalid request')
        return redirect('enroll.index')

def get_total_amount(request):
    course_id = request.GET.get('course_id')
    if course_id:
        try:
            course = Course.objects.get(id=course_id)
            return JsonResponse({'total_amount': course.total_amount})
        except Course.DoesNotExist:
            return JsonResponse({'total_amount': 0}, status=404)
    return JsonResponse({'total_amount': 0}, status=400)

def create_enroll(request):
    if request.method == 'POST':
        form = CreateEnrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enroll.index')  # Adjust the redirect as necessary
    else:
        form = CreateEnrollForm()

    return render(request, 'enrollment/enroll_form.html', {'form': form})

def update_enroll(request, pk):
    enroll = get_object_or_404(Enroll, pk=pk)
    if request.method == 'POST':
        form = CreateEnrollForm(request.POST, instance=enroll)
        if form.is_valid():
            form.save()
            return redirect('enroll.index')  # Adjust the redirect as necessary
    else:
        form = CreateEnrollForm(instance=enroll)

    return render(request, 'enrollment/enroll_form.html', {'form': form})
