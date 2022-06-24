from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Plant, Pot
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import WateringForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os

# Classes here.
class PlantCreate(LoginRequiredMixin, CreateView):
    model = Plant
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlantUpdate(LoginRequiredMixin, UpdateView):
    model = Plant
    fields = '__all__'

class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    success_url = '/plants/'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def plants_index(request):
    plants = Plant.objects.filter(user = request.user)
    return render(request, 'plants/index.html', {'plants': plants})

@login_required
def plants_detail(request, plant_id):
    watering_form = WateringForm()
    plant = Plant.objects.get(id=plant_id)
    pots_plant_doesnt_have = Pot.objects.exclude(id__in = plant.pots.all().values_list('id'))
    return render(request, 'plants/details.html', {'plant': plant, 'watering_form': watering_form, 'pots': pots_plant_doesnt_have})

@login_required
def add_watering(request, plant_id):
    form = WateringForm(request.POST)

    if form.is_valid():
        new_watering = form.save(commit=False)
        new_watering.plant_id = plant_id
        new_watering.save()
        return redirect('plantsDetail', plant_id = plant_id)

class PotList(LoginRequiredMixin, ListView):
    model = Pot

class PotDetail(LoginRequiredMixin, DetailView):
    model = Pot

class PotCreate(LoginRequiredMixin, CreateView):
    model = Pot
    fields = '__all__'

class PotUpdate(LoginRequiredMixin, UpdateView):
    model = Pot
    fields = '__all__'

class PotDelete(LoginRequiredMixin, DeleteView):
    model = Pot
    success_url = '/pots/'

@login_required
def assoc_pot(request, plant_id, pot_id):
    Plant.objects.get(id=plant_id).pots.add(pot_id)
    return redirect('plantsDetail', plant_id=plant_id)

@login_required
def unassoc_pot(request, plant_id, pot_id):
    Plant.objects.get(id=plant_id).pots.remove(pot_id)
    return redirect('plantsDetail', plant_id=plant_id)

def signup(request):
    error_message = ''

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('plantsIndex')
        else:
            error_message = 'Invalid Signup - Please try again later'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)