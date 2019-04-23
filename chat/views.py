from django.shortcuts import render

from .models import Message
from landing.models import Friend


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    chat_messages = Message.objects.filter(group_name=room_name).order_by("created")[:100]
    return render(request, 'chat/room.html', {
        'chat_messages': chat_messages,
        'room_name': room_name,

    })