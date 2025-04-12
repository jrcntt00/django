from django.shortcuts import render
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
        print(request.POST)

    return render(request, 'home/room_form.html', context)
