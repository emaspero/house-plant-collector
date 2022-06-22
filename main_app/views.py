from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Plant
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import WateringForm

# Classes here.
class PlantCreate(CreateView):
    model = Plant
    fields = '__all__'

class PlantUpdate(UpdateView):
    model = Plant
    fields = '__all__'

class PlantDelete(DeleteView):
    model = Plant
    success_url = '/plants/'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def plants_index(request):
    plants = Plant.objects.all()
    return render(request, 'plants/index.html', {'plants': plants})

def plants_detail(request, plant_id):
    watering_form = WateringForm()
    plant = Plant.objects.get(id=plant_id)
    return render(request, 'plants/details.html', {'plant': plant, 'watering_form': watering_form})

def add_watering(request, plant_id):
    form = WateringForm(request.POST)

    if form.is_valid():
        new_watering = form.save(commit=False)
        new_watering.plant_id = plant_id
        new_watering.save()
        return redirect('plantsDetail', plant_id = plant_id)