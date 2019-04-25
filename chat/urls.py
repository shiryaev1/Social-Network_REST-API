from django.urls import path, re_path

from chat import views

urlpatterns = [
    # path('', views.index, name='chat'),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
