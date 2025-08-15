# Create your views here.

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import MyUserCreationForm, RoomForm, UserForm
from .models import Message, Room, Topic, User
from .turbo import turbo_stream

# rooms = [
#   {"id":  1, "name": "Lets learn python!"},
#   {"id":  2, "name": "Design with me"},
#   {"id":  3, "name": "Frontend developer"}
# ]


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)  # add session in database and browser
            return redirect("home")
        else:
            messages.error(request, "email OR password does not exist")
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def registerPage(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(
                commit=False
            )  # save form and freez it in time/ not save in database yet
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured during registration")

    return render(request, "base/login_register.html", {"form": form})


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)  # OR statement
        | Q(description__icontains=q)
    )  # __contains(case sensitive ) ___icontains(not case sensitive)

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    # .order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)

        # Check if this is a Turbo request
        if request.headers.get("Accept", "").startswith("text/vnd.turbo-stream"):
            # Return Turbo Stream response
            message_html = f"""
        <div class="thread">
          <div class="thread__top">
            <div class="thread__author">
              <div class="avatar avatar--small">
                <img src="{request.user.avatar.url}" />
              </div>
              <div class="thread__authorInfo">
                <a href="/profile/{request.user.id}/">{request.user.name}</a>
                <span>just now</span>
              </div>
            </div>
          </div>
          <div class="thread__details">
            <p>{message.body}</p>
          </div>
        </div>
      """
            return turbo_stream(
                "append", "room-messages", message_html, request=request
            )

        return redirect("room", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")
    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("you are not allowed!!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.description = request.POST.get("description")
        room.topic = topic
        room.save()
        return redirect("home")

    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("you are not allowed!!")

    if request.method == "POST":
        room.delete()
        return redirect("home")

    context = {"obj": room.name}
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("you are not allowed!!")

    if request.method == "POST":
        message.delete()
        return redirect("home")

    context = {"obj": message.body}
    return render(request, "base/delete.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", pk=user.id)
    return render(request, "base/update-user.html", {"form": form})


def topicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "base/topics.html", {"topics": topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, "base/activity.html", {"room_messages": room_messages})
