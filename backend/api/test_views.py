from django.test import TestCase, Client
from django.urls import reverse
from api.models import *
from django.contrib.auth import get_user_model
from django.contrib import auth
# from django.contrib.auth.models import User
import json
import datetime

class TestViews(TestCase):
    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.home_url = reverse('home')
        self.all_bicycles_url = reverse('bicycles')
        self.bicycle_url = reverse('bicycle', args=['cannondale-scalpel-ht'])
        self.sign_in_url = reverse('sign_in')
        self.logout_url = reverse('logout')
        self.registrate_url = reverse('registrate')
        self.my_bicycles_url = reverse('my_bicycles')
        self.my_one_bicycle_url = reverse('my_one_bicycle', args=[1])
        self.bicycle1 = Bicycle.objects.create(
            brand = "Cannondale",
            model = "Scalpel HT",
            type = "Cross Country",
            wheel_size = 29,
            fork = "Rock Shox SID",
            description = "Best of the best",
            price = 15,
            image1 = "images/bicycles/cannondale-scalpel-ht-1_vx8ptsW.jpg",
            image2 = "images/bicycles/cannondale-scalpel-ht-2_zp5iTqh.jpg",
            image3 = "images/bicycles/cannondale-scalpel-ht-3.jpg",
        )
        self.user1 = User.objects.create_user(
            username = "imakeks",
            password = "trailking201",
            first_name = 'Makeks',
            last_name = 'Krutt'
        )


    def test_sign_in_GET(self):
        response = self.client.get(self.sign_in_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/sign_in.html')


    def test_sign_in_POST(self):
        pass
        # response = self.client.post(self.sign_in_url, self.user1, follow=True)

        # print("............" + str(response.context))
        # self.assertEquals(response.status_code, 302)
        # self.assertEquals(response.context['user'].is_active)


    def test_home_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/index.html')


    def test_all_bicycles_GET(self):
        response = self.client.get(self.all_bicycles_url)
        self.assertEquals(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'api/bicycles.html')


    def test_show_bicycle_GET_creates_renting(self):
        response = self.client.get(self.bicycle_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/bicycle.html')


    def test_show_bicycle_POST_creates_renting(self):
        User = get_user_model()
        self.client.login(username='imakeks', password='trailking201')
        user = auth.get_user(self.client)
        print("............" + str(user.is_authenticated))
        response = self.client.post(self.bicycle_url, follow=True, data={
            'bicycle': self.bicycle1,
            'user': self.user1,
            'time_get': datetime.datetime(2022, 6, 23, 8, 0, tzinfo=datetime.timezone.utc),
            'time_return': datetime.datetime(2022, 6, 24, 14, 0, tzinfo=datetime.timezone.utc),
            'total_price': 450,
            'status': True
        })

        self.assertEquals(response.status_code, 302)
        print("............" + str(self.user1))
        print("............" + str(self.user1.bicycles))
        print("............" + str(self.bicycle1))
        print("............" + str(self.bicycle1.renting_users))
        print("............" + str(response.content))
        # print("............" + str(self.user1))
        # print("............" + str(self.user1.profile))
        self.assertEquals(self.user1.bicycles.first().bicycle, self.bicycle1)

    # RentingInfo.objects.create(bicycle= Bicycle.objects.get(model="Scalpel HT"),user = User.objects.get(username='test_imakeks'),time_get = datetime.datetime(2022, 6, 2, 8, 0, tzinfo=datetime.timezone.utc),time_return = datetime.datetime(2022, 6, 3, 14, 0, tzinfo=datetime.timezone.utc),total_price = 450,status = True)
    # Bicycle.objects.create(brand = "Cannondale", model = "Scalpel HT", type = "Cross Country", wheel_size = 29, fork = "Rock Shox SID", description = "Best of the best", price = 15)

    def test_show_bicycle_POST_no_data(self):
        User = get_user_model()
        self.client.login(username='imakeks', password='trailking201')
        response = self.client.post(self.bicycle_url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.bicycle1.renting_users.count(), 0)



    def test_registrate_user_GET(self):
        response = self.client.get(self.registrate_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/registrate.html')


    def test_registrate_user_POST(self):
        User = get_user_model()
        count = User.objects.count()
        response = self.client.post(self.registrate_url, data={
            'username': 'imakuks',
            'password1': 'trailking201',
            'password2': 'trailking201',
            'first_name': 'Maks',
            'last_name': 'Krut'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEqual(User.objects.count(), count+1)


    def test_registrate_user_POST_no_data(self):
        User = get_user_model()
        count = User.objects.count()
        response = self.client.post(self.registrate_url)

        self.assertEquals(response.status_code, 200)
        self.assertEqual(User.objects.count(), count)


    def test_my_one_bicycle_GET(self):
        User = get_user_model()
        self.client.login(username='imakeks', password='trailking201')
        response = self.client.get(self.my_one_bicycle_url)
        self.assertEquals(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'api/my_bicycle.html')


    def test_my_one_bicycle_POST(self):
        User = get_user_model()
        self.client.login(username='imakeks', password='trailking201')
        response = self.client.post(self.bicycle_url, follow=True, data={
            'bicycle': self.bicycle1,
            'user': self.user1,
            'time_get': datetime.datetime(2022, 6, 24, 8, 0, tzinfo=datetime.timezone.utc),
            'time_return': datetime.datetime(2022, 6, 25, 14, 0, tzinfo=datetime.timezone.utc),
            'total_price': 450,
            'status': True
        })


    def test_my_bicycles_GET(self):
        response = self.client.get(self.my_bicycles_url)
        self.assertEquals(response.status_code, 200)
        
        self.assertTemplateUsed(response, 'api/my_bicycles.html')

    # def test_rent_bicycle_POST(self):
    #     response = self.client.post(self.bicycle, {
    #         'brand': "Cube",
    #         'model': "Stereo 170",
    #         'type': "Enduro",
    #         'wheel_size': 29,
    #         'fork': "FOX 34",
    #         'description': "Hmmm... OK",
    #         'price': 20,
    #     })

    #     bicycle2 = Bicycle.objects.get(id=2)
    #     self.assertEquals(bicycle2.model, 'Stereo 170')