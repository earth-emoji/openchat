import simplejson as json
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Room, Message
from .seralizers import RoomSerializer
from accounts.models import UserProfile

# Create your views here.
def index(request, template_name="rooms/index.html", data={}):
    data['rooms'] = Room.objects.all()
    return render(request, template_name, data)

def room(request, url, template_name="rooms/details.html", data={}):
    profile = UserProfile.objects.get(user=request.user)
    room = Room.objects.get(url=url)

    # check if user is in room
    if room.host == profile or room.members.filter(pk=profile.id).exists():
        data['room'] = room
        data['messages'] = Message.objects.filter(room=room)
        return render(request, template_name, data)
    else:
        messages.info(request, 'You must join this room to enter.')
        return redirect(reverse('rooms:index'))


@api_view(['GET', 'POST'])
def room_collection(request):
    if request.method == 'GET':
        rooms = Room.objects.filter(host=request.user.profile)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {
            'name': request.data.get('name'),
            'host': request.user.profile.pk
        }
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def join_room(request):
    # user clicks the join button and the user is added to the group
    if request.method == 'POST':
        room = Room.objects.get(slug=request.POST['room'])
        room.members.add(request.user.profile)
        data = {
            'success': f"You have joined {room.name}, <a href='/rooms/{room.url}/'>start chatting now</a>"
        }
        return JsonResponse(data)
     # return response
    return HttpResponse('')