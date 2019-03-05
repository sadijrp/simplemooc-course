from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages

from .models import Thread
from .forms import ReplyForm


class ForumView(ListView):
    paginate_by = 2
    template_name = 'index.html'

    def get_queryset(self):
        queryset = Thread.objects.all()
        order = self.request.GET.get('order', '')

        if order == 'views':
            queryset = queryset.order_by('-views')
        elif order == 'answers':
            queryset = queryset.order_by('-answers')

        if 'tag' in self.kwargs:
            tag = self.kwargs['tag']
            queryset = queryset.filter(tags__slug__in=[tag])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        return context


class ThreadView(DetailView):
    model = Thread
    template_name = 'thread.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        context['form'] = ReplyForm(self.request.POST or None)
        return context

    def get(self, request, *args, **kwargs):
        response = super(ThreadView, self).get(request, *args, **kwargs)
        if not request.user.is_authenticated or \
           (self.object.author != request.user):
            self.object.views = self.object.views + 1
            self.object.save()
        return response

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,
                           'Voce deve estar logado  adicionar uma resposta')
            return redirect(request.path)

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form']
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = self.object
            reply.author = request.user
            reply.save()
            messages.success(request, 'Resposta criada com sucesso')
            context['form'] = ReplyForm
        return self.render_to_response(context)
