from django.shortcuts import render
from django.views.generic import ListView

from .models import Thread


class ForumView(ListView):
    model = Thread
    paginate_by = 10
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        return context
