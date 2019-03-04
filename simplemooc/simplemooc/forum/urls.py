from django.urls import path, re_path
from . import views


app_name = 'forum'

urlpatterns = [
    path('', views.ForumView.as_view(), name='index'),
    re_path(r'^tag/(?P<tag>[\w_-]+)',
            views.ForumView.as_view(),
            name='tagged_index'),
    ]
