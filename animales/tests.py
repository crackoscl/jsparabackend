import json

from django.test import TestCase, Client
from urllib.parse import urlencode

from .forms import AnimalForm
from .models import Animales

from django.contrib.auth.models import User


class AnimalesTestCase(TestCase):

    def setUp(self):
        animales = Animales.objects.create(
            especie="Malamute",
            nombre="Los Jacos",
            numero=3,
            comida=6,
            user_id=1
        )
        animales.save()
        self.client = Client()
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.login(username='testuser', password='12345')

    def test_user_is_able_to_login(self) -> None:
        logged_in = self.client.login(username='testuser', password='12345')
        self.assertEqual(True, logged_in)

    def test_validar_form(self) -> None:
        data = {'especie': 'Focas', 'nombre': 'Los Manolos', 'numero': 3, 'comida': 2, 'user_id': 1}
        form = AnimalForm(data=data)
        self.assertTrue(form.is_valid())

    def test_crear_fila_de_animales(self):
        data = {'especie': 'Foca', 'nombre': 'Las Focas', 'numero': 3, 'comida': 2, 'user_id': 1}
        self.client.post("/animales/", urlencode(data),
                         content_type="application/x-www-form-urlencoded")
        foca = Animales.objects.get(especie='Foca')
        self.assertEqual('Foca', foca.especie)

    def test_borrar_fila_de_tabla_animales(self):
        perros = Animales.objects.get(especie='Malamute', nombre='Los Jacos')
        self.assertEqual(perros.id, 1)
        perros = Animales.objects.filter(especie='Malamute')
        self.assertEqual(1, perros.count())
        response = self.client.post('/animales/delete/1')
        json_response = json.loads(response.content)
        self.assertEqual(1, json_response['row_deleted'])
        self.assertEquals(200, response.status_code)
        perros = Animales.objects.filter(especie='Malamute')
        # has been deleted
        self.assertEquals(0, perros.count())

    def test_nuevo_endpoint_para_nuevos_animales(self):
        json_string = '{}'
        json_data = json.loads(json_string)
        response = self.client.post('/animales/new', json_data, content_type='application/json')
        self.assertEqual(400, response.status_code)
        json_string = '{"especie": "Perro", "nombre": "perro test", "numero": "2", "comida": "1", "user_id": "1000"}'
        json_data = json.loads(json_string)
        response = self.client.post('/animales/new', json_data, content_type='application/json')
        animalitos = Animales.objects.all()
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(animalitos))
        json_response = json.loads(response.content)
        self. assertEqual(2, json_response["id_saved"])

    def test_nuevo_endpoint_para_actualizar_records(self):
        # get a record
        unAnimal = Animales.objects.filter(id=1)
        # check we have a record stored
        self.assertEqual(1, len(unAnimal))
        self.assertEqual("Los Jacos", unAnimal[0].nombre)
        self.assertEqual(1, unAnimal[0].id)
        json_string = '{"id": 1, "especie": "Perro", "nombre": "juanito", \
                        "numero": 2, "comida": 4, "user_id": 1}'
        json_data = json.loads(json_string)
        response = self.client.post('/animales/update', json_data, content_type='application/json')
        # # Testing at DB level get updated record
        otroAnimal = Animales.objects.filter(id=1)
        self.assertEqual("juanito", otroAnimal[0].nombre)
        respuesta = json.loads(response.content)
        self.assertEqual(json_data, respuesta)
