from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from .models import Course
from .forms import ContactCourse
from django.core import mail


class ContactCourseTestCase(TestCase):

    def setUp(self):
        self.course = Course.objects.create(name="Test", slug="test")
    
    def tearDown(self):
        self.course.delete()
    
    def test_contact_form_error(self):
        data = {
            "name": "Joao da Silva",
            "email": "",
            "msg": ""
        }

        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'msg', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')

    def test_contact_form_success(self):
        data = {
            "name": "Joao da Silva",
            "email": "joao@joao.com",
            "msg": "Faltou a ementa"
        }

        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertEqual(len(mail.outbox), 1)
        


    def test_form(self):
        form_data = {'something': 'something'}
        form = ContactCourse({"name":"joao", "email":"joao@joao.com", "msg":"alalalal"})
        self.assertTrue(form.is_valid())