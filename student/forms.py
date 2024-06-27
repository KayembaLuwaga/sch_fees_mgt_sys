from django import forms
from student.models import Student


class CreateStudentForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    student_number = forms.CharField(label='Student Number', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))  # Stdnt_No
    std_class = forms.CharField(label='Class', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))  # Class
    stream = forms.CharField(label='Stream', max_length=200, widget=forms.Textarea(attrs={'class': 'form-control'}))  # Stream

    class Meta:
        model = Student
        fields = ['name', 'student_number', 'std_class', 'stream']
