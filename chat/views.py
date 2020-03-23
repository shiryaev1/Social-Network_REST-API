from django.shortcuts import render, Http404
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Message


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    fid, sid = room_name.split('_')
    fid, sid = int(fid), int(sid)
    if request.user.id != fid and request.user.id != sid:
        raise Http404('There is no such chat')
    myself = request.user
    companion = User.objects.get(id=sid)
    companions = User.objects.exclude(message__isnull=True).exclude(
        message__user=request.user
    )
    chat_messages = Message.objects.filter(
        group_name=room_name
    ).order_by("created")[:100]

    return render(request, 'my_profile/test.html', {
        'chat_messages': chat_messages,
        'room_name': room_name,
        'myself': myself,
        'companion': companion,
        'companions': companions,
        # 'room': reverse('room', kwargs={'room_name': room_name}),

    })
