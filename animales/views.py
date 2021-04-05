from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth import get_user_model

from animales.forms import AnimalForm
from animales.models import Animales
import json


def add_animal(request):
    template_name = "animales/animales.html"
    User = get_user_model()
    user_id = request.user.id
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            especie = request.POST['especie']
            nombre = request.POST['nombre']
            numero = int(request.POST['numero'])
            if especie == 'Perro':
                comida = 2 * numero
            elif especie == 'Cocodrilo':
                comida = 5 * numero
                # else means especie == 'Gato':
            else:
                comida = numero
            animal = Animales(
                especie=especie, nombre=nombre, numero=numero, comida=comida,
                user_id=user_id
            )
            animal.save()

            # Avoid submitting on refreshing page
            return HttpResponseRedirect('/animales')
        else:
            print(form.errors.as_data())
            form = AnimalForm()
    else:
        # GET do nothing
        pass
    animales = Animales.objects.all()
    total_comida = 0
    for animal in animales:
        total_comida += int(animal.comida)
    form = AnimalForm()
    users = User.objects.all()
    alimentadores = {}
    for user in users:
        user_animals = animales.filter(user_id=user.id)
        alimentadores[user.username] = 0
        for user_animal in user_animals:
            alimentadores[user.username] += user_animal.comida

    return render(request, template_name, {
        'form': form,
        'animales': animales,
        'total_comida': total_comida,
        'alimentadores': alimentadores
        }
    )


def delete_animal(request, id):
    if request.method == 'POST':
        row = Animales.objects.get(id=id)
        row.delete()
        return JsonResponse({'row_deleted': id})
    else:
        return JsonResponse({'message': 'method not allowed'})


def new_animal(request):
    data = request.POST
    body = json.loads(request.body)
    if not body:
        return HttpResponseBadRequest()
    else:
        form = AnimalForm(body)
        if form.is_valid():
            especie = body['especie']
            numero = body['numero']
            if especie == 'Perro':
                comida = 2 * numero
            elif especie == 'Cocodrilo':
                comida = 5 * numero
                # else means especie == 'Gato':
            else:
                comida = numero
            animal = Animales(
                especie=especie, nombre=body["nombre"],
                numero=numero, comida=comida,
                user_id=body['user_id']
            )
            animal.save()
            return JsonResponse({'id_saved': animal.id})
        else:
            return HttpResponseBadRequest()


def update_animal(request):
    print(request.body)
    body = json.loads(request.body)
    Animales.objects.all().filter(id=body['id']).update(
        especie=body['especie'],
        nombre=body['nombre'],
        numero=body['numero'],
        comida=body['comida']
    )
    try:
        record = Animales.objects.all().filter(id=body['id'])[0]
        record.save()
    except:
        return JsonResponse({'message': 'something went wrong'})
    return JsonResponse({
        'id': record.id,
        'especie': record.especie,
        'nombre': record.nombre,
        'numero': record.numero,
        'comida': record.comida,
        'user_id': record.user_id
    })
