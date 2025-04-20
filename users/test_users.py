import pytest
from django.test import Client
from django.urls import reverse

from users.models import Admin, Manager, Student, Teacher


@pytest.mark.django_db
class TestAdminAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.admin = Admin.objects.create(
            first_name="admin1",
            phone="01012070620",
            password="admin",
            email="admin1@gmail.com",
        )
        self.client = Client()
        self.url_list = reverse("admins-list")
        self.url_detail = reverse("admins-detail", args=[self.admin.id])

    def test_list_admin(self):
        response = self.client.get(self.url_list)
        assert response.status_code == 200

    def test_create_admin(self):
        data = {
            "first_name": "admin1",
            "phone": "01012070620",
            "password": "admin",
            "email": "admin1@gmail.com",
        }
        response = self.client.post(
            self.url_list, data=data, content_type="application/json"
        )
        assert response.status_code == 201

    def test_update_admin(self):
        update_data = {
            "first_name": "admin1",
            "phone": "01012070620",
            "password": "admin",
            "email": "admin1@gmail.com",
        }
        response = self.client.put(
            self.url_detail, data=update_data, content_type="application/json"
        )
        assert response.status_code == 200

    def test_retrieve_admin(self):
        update_data = {
            "first_name": "admin1",
            "phone": "01012070620",
            "password": "admin",
            "email": "admin1@gmail.com",
        }
        response = self.client.patch(
            self.url_detail, data=update_data, content_type="application/json"
        )
        assert response.status_code == 200

    def test_delete_admin(self):
        response = self.client.delete(self.url_detail)
        assert response.status_code == 204


@pytest.mark.django_db
class TestManagerAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.manager = Manager.objects.create(
            first_name="manager1",
            phone="01012070620",
            password="manager",
            email="manager1@gmail.com",
        )
        self.client = Client()
        self.url_list = reverse("managers-list")
        self.url_detail = reverse("managers-detail", args=[self.manager.id])

    def test_list_manager(self):
        response = self.client.get(self.url_list)
        assert response.status_code == 200

    def test_create_manager(self):
        data = {
            "first_name": "manager1",
            "phone": "01012070620",
            "password": "manager",
            "email": "manager1@gmail.com",
        }
        response = self.client.post(
            self.url_list, data=data, content_type="application/json"
        )
        assert response.status_code == 201

    def test_update_manager(self):
        update_data = {
            "first_name": "manager1",
            "phone": "01012070620",
            "password": "manager",
            "email": "manager@gmail.com",
        }
        response = self.client.put(
            self.url_detail, data=update_data, content_type="application/json"
        )
        assert response.status_code == 200

    def test_retrieve_manager(self):
        update_data = {
            "first_name": "manager1",
            "phone": "01012070620",
            "password": "manager1",
            "email": "manager1@gmail.com",
        }
        response = self.client.patch(
            self.url_detail, data=update_data, content_type="application/json"
        )
        assert response.status_code == 200

    def test_delete_manager(self):
        response = self.client.delete(self.url_detail)
        assert response.status_code == 204


@pytest.mark.django_db
class TestTeacherAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.teacher = Teacher.objects.create(
            first_name="teacher1",
            phone="01012070620",
            password="teacher",
            email="teacher1@gmail.com",
        )
        self.client = Client()
        self.url_list = reverse("teachers-list")
        self.url_detail = reverse("teachers-detail", args=[self.teacher.id])

    def test_list_teacher(self):
        response = self.client.get(self.url_list)
        assert response.status_code == 200

    def test_create_teacher(self):
        data = {
            "first_name": "teacher1",
            "phone": "01012070620",
            "password": "teacher",
            "email": "teacher1@gmail.com",
        }
        response = self.client.post(
            self.url_list, data=data, content_type="application/json"
        )
        assert response.status_code == 201

    def test_update_teacher(self):
        update_data = {
            "first_name": "teacher1",
            "phone": "01012070620",
            "password": "teacher",
            "email": "teacher1@gmail.com",
        }
        response = self.client.put(
            self.url_detail, data=update_data, content_type="application/json"
        )
        assert response.status_code == 200

    def test_retrieve_teacher(self):
        update_data = {
            "first_name": "teacher1",
            "phone": "01012070620",
            "password": "teacher1",
            "email": "teacher1@gmail.com",
        }
        response = self.client.patch(
            self.url_detail, data=update_data, content_type="application/json"
        )
        assert response.status_code == 200

    def test_delete_teacher(self):
        response = self.client.delete(self.url_detail)
        assert response.status_code == 204


@pytest.mark.django_db
class TestStudentAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.student = Student.objects.create(
            first_name="student1",
            phone="01012070620",
            password="student",
            email="student1@gmail.com",
            parent_phone="01102015693",
        )
        self.client = Client()
        self.url_list = reverse("students-list")
        self.url_detail = reverse("students-detail", args=[self.student.id])

    def test_list_student(self):
        response = self.client.get(self.url_list)
        assert response.status_code == 200

    def test_create_student(self):
        data = {
            "first_name": "student1",
            "phone": "01012070620",
            "password": "student",
            "email": "student1@gmail.com",
            "parent_phone": "01102015693",
        }
        response = self.client.post(
            self.url_list, data=data, content_type="application/json"
        )
        assert response.status_code == 201

    def test_update_student(self):
        update_data = {
            "first_name": "student1",
            "phone": "01012070620",
            "password": "student",
            "email": "student1@gmail.com",
            "parent_phone": "01102015693",
        }
        response = self.client.put(
            self.url_detail, data=update_data, content_type="application/json"
        )
        assert response.status_code == 200

    def test_retrieve_student(self):
        update_data = {
            "first_name": "student1",
            "phone": "01012070620",
            "password": "student1",
            "email": "student1@gmail.com",
            "parent_phone": "01102015693",
        }
        response = self.client.patch(
            self.url_detail, data=update_data, content_type="application/json"
        )
        assert response.status_code == 200

    def test_delete_student(self):
        response = self.client.delete(self.url_detail)
        assert response.status_code == 204
