from .models import Appointment
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.models import Group
import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_KEY", None)


def chatbot(request):
    chatbot_response = None
    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        user_input = request.POST.get('user_input')
        prompt = f" {user_input}"

        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=250,
            stop=".",
            temperature=0.5
        )
        print(response)

        chatbot_response = response["choices"][0]["text"]

    return render(request, 'chatbot.html', {"response": chatbot_response})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = request.POST.get('group')
            selected_group = Group.objects.get(name=group)
            user.groups.add(selected_group)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('/')
        else:
            form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')


def index(request):
    return render(request, 'index.html')


def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            return redirect('../')
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})


def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'edit_appointment.html', {'form': form})


def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('profile')
    return render(request, 'delete_appointment.html', {'appointment': appointment})
