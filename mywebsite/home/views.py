from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# rooms =[
#     {'id': 1, 'name':'Lets learn python!'},
#     {'id': 2, 'name':'Design with me'},
#     {'id': 3, 'name':'Fontend developers'},
# ] 


def index(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'home/home.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}      
    return render(request,'home/room.html',context)

def createRoom(request):

    form = RoomForm()
    context={'form':form}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'home/room_form.html', context)


def updateRoom(request ,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form':form}
    return render(request,'home/room_form.html', context)