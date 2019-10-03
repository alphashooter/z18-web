from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.test import TestCase, LiveServerTestCase
from selenium.webdriver import Chrome
from time import sleep

# Create your tests here.


# class LoginTest(TestCase):
#     def setUp(self) -> None:
#         super().setUp()
#         User.objects.create_user('bob', password='bob')
#
#     def test_login_get(self):
#         response: HttpResponse = self.client.get('/login')
#         self.assertEqual(response.status_code, 200)
#
#     def test_login_post(self):
#         response: HttpResponse = self.client.post('/login', b'username=bob&password=bob', content_type='application/x-www-form-urlencoded')
#         self.assertEqual(response.status_code, 302)


class SeleniumTestCase(LiveServerTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.driver = Chrome(r'D:\env\selenium\chromedriver.exe')

    def tearDown(self) -> None:
        super().tearDown()
        self.driver.quit()


class LoginTest2(SeleniumTestCase):
    def setUp(self) -> None:
        super().setUp()
        User.objects.create_user('bob', password='bob')

    def test(self):
        self.driver.get(self.live_server_url + '/login')
        sleep(2)
        username = self.driver.find_element_by_id('input-username')
        password = self.driver.find_element_by_id('input-password')
        submit = self.driver.find_element_by_id('input-submit')
        username.send_keys('bob')
        password.send_keys('bob')
        sleep(2)
        submit.click()
        self.assertEqual(self.driver.current_url, self.live_server_url + "/")
