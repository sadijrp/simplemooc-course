from django.shortcuts import render
from .models import Course

def index(request):
    courses = Course.objects.all()
    template = 'courses/index.html'

    context = {
        'courses': courses
    }

    return render(request, template, context)
