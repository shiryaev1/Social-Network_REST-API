from django.shortcuts import render, Http404

from .models import Message
from landing.models import Friend


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    fid, sid = room_name.split('_')
    fid, sid = int(fid), int(sid)
    if request.user.id != fid and request.user.id != sid:
        raise Http404('There is no such chat')
    myself = request.user
    chat_messages = Message.objects.filter(group_name=room_name).order_by("created")[:100]
    return render(request, 'chat/room.html', {
        'chat_messages': chat_messages,
        'room_name': room_name,
        'myself': myself

    })
