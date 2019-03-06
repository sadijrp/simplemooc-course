from django.urls import path, re_path

from . import views


app_name = 'forum'

urlpatterns = [
    path('', views.ForumView.as_view(), name='index'),
    re_path(r'^tag/(?P<tag>[\w_-]+)',
            views.ForumView.as_view(),
            name='tagged_index'),
    re_path(r'^respostas/(?P<pk>\d+)/correta/',
            views.CorrectReplyView.as_view(),
            name='correct_reply'),
    re_path(r'^respostas/(?P<pk>\d+)/incorreta/',
            views.CorrectReplyView.as_view(correct=False),
            name='incorrect_reply'),
    re_path(r'^(?P<slug>[\w_-]+)',
            views.ThreadView.as_view(),
            name='thread'),
    ]
