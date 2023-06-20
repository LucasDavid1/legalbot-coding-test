from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from societies.models import Society, Partner, Administrator, Faculty


class SocietyCreateViewTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
    
    def test_create_society(self):
        url = reverse('create-society')
        data = {
            'name': 'Test Society',
            'rut': '1234567890',
        }
        
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Society.objects.count(), 1)
        self.assertEqual(Society.objects.get().name, 'Test Society')
        self.assertEqual(Society.objects.get().rut, '1234567890')


class PartnerCreateViewTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.society = Society.objects.create(name='Test Society', rut='1234567890')

    def test_create_partner(self):
        url = reverse('create-partner')
        data = {
            'name': 'John Doe',
            'rut': '0987654321',
            'address': '123 Main St',
            'participation': '50.5',
            'society': self.society.id,
        }
        
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Partner.objects.count(), 1)
        self.assertEqual(Partner.objects.get().name, 'John Doe')
        self.assertEqual(Partner.objects.get().rut, '0987654321')
        self.assertEqual(Partner.objects.get().address, '123 Main St')
        self.assertEqual(Partner.objects.get().participation, 50.5)
        self.assertEqual(Partner.objects.get().society, self.society)


class AdministratorCreateViewTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.society = Society.objects.create(name='Test Society', rut='1234567890')

    def test_create_administrator_with_faculties(self):
        url = reverse('create-administrator')
        data = {
            'name': 'John Doe',
            'rut': '0987654321',
            'society': self.society.id,
            'faculties': [
                {'name': 'Abrir una cuenta corriente'},
                {'name': 'Firmar cheques'},
                {'name': 'Firmar contratos'},
            ],
        }

        self.client.login(username=self.username, password=self.password)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Administrator.objects.count(), 1)
        self.assertEqual(Administrator.objects.get().name, 'John Doe')
        self.assertEqual(Administrator.objects.get().rut, '0987654321')
        self.assertEqual(Administrator.objects.get().society, self.society)
        self.assertEqual(Faculty.objects.count(), 3)
        self.assertListEqual(
            list(Faculty.objects.values_list('name', flat=True)),
            ['Abrir una cuenta corriente', 'Firmar cheques', 'Firmar contratos']
        )


class SocietyRetrieveDeleteViewTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.society = Society.objects.create(name='Test Society', rut='1234567890')

    def test_retrieve_society(self):
        url = reverse('society-delete', kwargs={'rut': self.society.rut})

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Society')
        self.assertEqual(response.data['rut'], '1234567890')

    def test_delete_society(self):
        url = reverse('society-delete', kwargs={'rut': self.society.rut})

        self.client.login(username=self.username, password=self.password)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Society.objects.filter(rut='1234567890').exists())



class SocietyByPartnerViewTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.society1 = Society.objects.create(name='Society 1', rut='1234567890')
        self.society2 = Society.objects.create(name='Society 2', rut='0987654321')
        self.partner = Partner.objects.create(name='Partner', rut='1111111111', participation=0.0, society=self.society1)
        self.administrator = Administrator.objects.create(name='Administrator', rut='2222222222', society=self.society2)

    def test_get_societies_by_partner(self):
        url = reverse('society-by-partner', kwargs={'rut': self.partner.rut})

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Society 1')
        self.assertEqual(response.data[0]['rut'], '1234567890')

    def test_get_societies_by_administrator(self):
        url = reverse('society-by-partner', kwargs={'rut': self.administrator.rut})

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Society 2')
        self.assertEqual(response.data[0]['rut'], '0987654321')



class PartnersAdministratorsBySocietyViewTest(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.society = Society.objects.create(name='Test Society', rut='1234567890')
        self.partner1 = Partner.objects.create(name='Partner 1', rut='1111111111', participation=0.0, society=self.society)
        self.partner2 = Partner.objects.create(name='Partner 2', rut='2222222222', participation=0.0, society=self.society)
        self.administrator1 = Administrator.objects.create(name='Administrator 1', rut='3333333333', society=self.society)
        self.administrator2 = Administrator.objects.create(name='Administrator 2', rut='4444444444', society=self.society)

    def test_get_partners_and_administrators_by_society(self):
        url = reverse('partners-administrators-by-society', kwargs={'rut': self.society.rut})

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['partners']), 2)
        self.assertEqual(len(response.data[0]['administrators']), 2)
        self.assertEqual(response.data[0]['partners'][0]['name'], 'Partner 1')
        self.assertEqual(response.data[0]['partners'][0]['rut'], '1111111111')
        self.assertEqual(response.data[0]['partners'][1]['name'], 'Partner 2')
        self.assertEqual(response.data[0]['partners'][1]['rut'], '2222222222')
        self.assertEqual(response.data[0]['administrators'][0]['name'], 'Administrator 1')
        self.assertEqual(response.data[0]['administrators'][0]['rut'], '3333333333')
        self.assertEqual(response.data[0]['administrators'][1]['name'], 'Administrator 2')
        self.assertEqual(response.data[0]['administrators'][1]['rut'], '4444444444')
