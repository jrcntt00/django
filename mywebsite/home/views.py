from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# rooms =[
#     {'id': 1, 'name':'Lets learn python!'},
#     {'id': 2, 'name':'Design with me'},
#     {'id': 3, 'name':'Fontend developers'},
# ] 


def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User dose not exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request, "Username or password does not exist")

    context = {}
    return render(request, 'home/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def index(request):

    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains =q)|
        Q(name__icontains=q)|
        Q(description__icontains=q) 
        )

    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms, 'topics':topics, 'room_count': room_count}
    return render(request, 'home/home.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}      
    return render(request,'home/room.html',context)


@login_required(login_url='login')
def createRoom(request):

    form = RoomForm()
    context={'form':form}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'home/room_form.html', context)



@login_required(login_url='login')
def updateRoom(request ,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form':form}
    return render(request,'home/room_form.html', context)



@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here')


    if request.method =='POST':
        room.delete()
        return redirect('index')
    return render(request, 'home/delete.html', {'obj':room})