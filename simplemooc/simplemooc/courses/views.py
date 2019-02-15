from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Announcement
from .forms import ContactCourse, CommentForm


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
def announcements(request, slug):
    template_name = 'courses/announcements.html'
    context = {}

    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment,
            user=request.user,
            course=course
        )
        if not enrollment.is_approved():
            messages.error(request, "A sua inscrição está pendente.")
            return redirect('account:dashboard')

    context['course'] = course
    context['announcements'] = course.announcements.all()

    return render(request, template_name, context)


@login_required
def announcement(request, slug, pk):
    template_name = 'courses/announcement.html'
    context = {}

    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(
            Enrollment,
            user=request.user,
            course=course
        )
        if not enrollment.is_approved():
            messages.error(request, "A sua inscrição está pendente.")
            return redirect('account:dashboard')

    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        print(announcement.id, "ajsaskdjhaskdhask")
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, "Comentário adicionado!")

    context['course'] = course
    context['announcement'] = announcement
    context['form'] = form

    return render(request, template_name, context)
