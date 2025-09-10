from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Food, Consume
from .forms import RegisterForm, LoginForm


# ------------------------------
# Authentication Views
# ------------------------------

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("index")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "tracker/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back {username}!")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "tracker/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


# ------------------------------
# Calorie Tracker Views
# ------------------------------

@login_required
def index(request):
    if request.method == "POST":
        food_id = request.POST.get("food_consumed")
        food = Food.objects.get(id=food_id)
        Consume.objects.create(user=request.user, food_consumed=food)
        return redirect("index")  # refresh page to update table & chart

    foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)
    return render(request, "tracker/index.html", {"foods": foods, "consumed_food": consumed_food})


@login_required
def delete_consume(request, id):
    consumed_food = get_object_or_404(Consume, id=id, user=request.user)
    
    if request.method == "POST":
        consumed_food.delete()
    return redirect("index")
