from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment
from .forms import ContactCourse


def index(request):
    courses = Course.objects.all()
    template = 'courses/index.html'

    context = {
        'courses': courses
    }

    return render(request, template, context)


def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    template = 'courses/details.html'
    context = {}

    if request.method == "POST":
        form = ContactCourse(request.POST)
        if form.is_valid():
            context["is_valid"] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()

    context["course"] = course
    context["form"] = form

    return render(request, template, context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course)

    if created:
        enrollment.active()
        message = "Inscrição realizada com sucesso."
        messages.success(request, message)
    else:
        message = "Seu usuário ja está inscrito no curso."
        messages.info(request, message)

    return redirect('account:dashboard')
