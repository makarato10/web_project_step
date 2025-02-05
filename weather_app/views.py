from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import SearchHistory
from .forms import RegisterForm, LoginForm
import requests

API_KEY = '84ca2746b402e27620371c2761a09a4d'


def home(request):
    weather = None
    if request.method == 'POST':
        city = request.POST['city']
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'
        response = requests.get(url).json()

        if response.get('main'):
            weather = {
                'city': city,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description']
            }
            if request.user.is_authenticated:
                SearchHistory.objects.create(
                    user=request.user,
                    city=weather['city'],
                    temperature=weather['temperature'],
                    description=weather['description']
                )

    return render(request, 'main.html', {'weather': weather})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"error": "Неверные данные для входа"})

    return render(request, "login.html")



def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def history_view(request):
    history = SearchHistory.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "history.html", {"history": history})
