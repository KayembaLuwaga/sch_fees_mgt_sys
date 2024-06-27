# enrollment/forms.py
from django import forms
from course.models import Course
from enrollment.models import Enroll
from student.models import Student


class CreateEnrollForm(forms.ModelForm):
    student_id = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Student'
    )

    course_id = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Course'
    )

    total_fee = forms.FloatField(
        widget=forms.HiddenInput(),)

    class Meta:
        model = Enroll
        fields = ['student_id', 'course_id', 'total_fee']

    def __init__(self, *args, **kwargs):
        super(CreateEnrollForm, self).__init__(*args, **kwargs)
        self.fields['total_fee'].initial = 0  # Default to 0

        if self.instance and self.instance.pk:
            # If editing an existing enrollment, set the total_fee to match the course's total_amount
            self.fields['total_fee'].initial = self.instance.course_id.total_amount

        # Customize the label for student_id field
        self.fields['student_id'].label_from_instance = self.get_student_label

    def get_student_label(self, student):
        """Return a string for the student dropdown showing student_number - name"""
        return f"{student.student_number} - {student.name}"

    def save(self, commit=True):
        # Override the save method to set the total_fee to the course's total_amount
        enroll = super(CreateEnrollForm, self).save(commit=False)
        enroll.total_fee = enroll.course_id.total_amount

        if commit:
            enroll.save()

        return enroll
