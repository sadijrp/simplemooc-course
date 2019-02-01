from django.test import TestCase
from model_mommy import mommy
from django.test.client import Client
from simplemooc.courses.models import Course


class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.django_quantity = 3
        self.courses_django = mommy.make('courses.Course',
            name="python DJANGO", _quantity=self.django_quantity)
        self.dev_quantity = 5
        self.courses_dev = mommy.make('courses.Course',
            name="python DEV", _quantity=self.dev_quantity)
        self.client = Client()
    
    def tearDown(self):
        Course.objects.all().delete()
    
    def test_course_manager_search(self):
        search = Course.objects.search('django')
        self.assertEquals(len(search), self.django_quantity)
        
        search = Course.objects.search('dev')
        self.assertEquals(len(search), self.dev_quantity)

        search = Course.objects.search('python')
        self.assertEquals(len(search), self.django_quantity + self.dev_quantity)