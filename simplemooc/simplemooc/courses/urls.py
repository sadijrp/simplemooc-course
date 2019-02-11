from django.urls import path, re_path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<slug>[\w_-]+)/$', views.details, name='details'),
    re_path(r'^(?P<slug>[\w_-]+)/inscricao/$',
            views.enrollment,
            name='enrollment'),
    re_path(r'^(?P<slug>[\w_-]+)/anuncios/$',
            views.announcements,
            name='announcements'),
    re_path(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$',
        views.undo_enrollment,
        name='undo_enrollment'),
]
