from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement, Lesson, Material
from .forms import ContactCourse, CommentForm
from .decorators import enrollment_required


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


@login_required
def undo_enrollment(request, slug):
    template_name = "courses/undo_enrollment.html"
    context = {}

    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
            Enrollment,
            user=request.user,
            course=course
        )

    if request.method == "POST":
        enrollment.delete()
        msg = "Sua inscrição foi cancelada com sucesso."
        messages.success(request, msg)
        return redirect("account:dashboard")

    context['enrollment'] = enrollment
    context['course'] = course

    return render(request, template_name, context)


@login_required
@enrollment_required
def announcements(request, slug):
    template_name = 'courses/announcements.html'
    context = {}
    course = request.course

    context['course'] = course
    context['announcements'] = course.announcements.all()

    return render(request, template_name, context)


@login_required
@enrollment_required
def announcement(request, slug, pk):
    template_name = 'courses/announcement.html'
    context = {}
    course = request.course
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, "Comentário adicionado!")

    context['course'] = course
    context['announcement'] = announcement
    context['form'] = form

    return render(request, template_name, context)


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template_name = 'courses/lessons.html'
    lessons = course.released_lessons

    if request.user.is_staff:
        lessons = course.lessons.all()

    context = {
        'course': course,
        'lessons': lessons
    }

    return render(request, template_name, context)


@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    template_name = 'courses/lesson.html'
    lesson = get_object_or_404(Lesson, pk=pk, course=course)

    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não está disponível')
        return redirect('courses:lessons', slug=course.slug)

    context = {
        'course': course,
        'lesson': lesson
    }

    return render(request, template_name, context)


@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    template_name = "courses/material.html"
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson

    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Este material não está disponível')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)

    if not material.is_embedded:
        return redirect(material.file.url)

    context = {
        'course': course,
        'lesson': lesson,
        'material': material
    }

    return render(request, template_name, context)
