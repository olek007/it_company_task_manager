from django.test import TestCase
from datetime import date, timedelta

from task_manager.forms import (
    SignUpForm,
    WorkerCreateForm,
    WorkerUpdateForm,
    ProjectForm,
    TaskForm,
    NameSearchForm,
)
from task_manager.models import Worker, Team, Position, Project, TaskType, Task


class SignUpFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }

    def test_valid_form(self):
        form = SignUpForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        data = self.valid_data.copy()
        data["password2"] = "wrongpassword"
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_user_saved(self):
        form = SignUpForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.valid_data["username"])
        self.assertTrue(user.check_password(self.valid_data["password1"]))


class WorkerFormMixin:
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")
        cls.team = Team.objects.create(name="Alpha Team")
        cls.base_data = {
            "username": "newworker",
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "password1": "securepass123",
            "password2": "securepass123",
            "position": cls.position.id,
            "team": cls.team.id,
        }


class WorkerCreateFormTest(WorkerFormMixin, TestCase):
    def test_valid_form(self):
        form = WorkerCreateForm(data=self.base_data)
        self.assertTrue(form.is_valid())

    def test_missing_names(self):
        data = self.base_data.copy()
        data["first_name"] = ""
        data["last_name"] = ""
        form = WorkerCreateForm(data=data)
        self.assertFalse(form.is_valid())
        for field in ["first_name", "last_name"]:
            with self.subTest(field=field):
                self.assertIn(field, form.errors)

    def test_worker_created(self):
        form = WorkerCreateForm(data=self.base_data)
        self.assertTrue(form.is_valid())
        worker = form.save()
        self.assertEqual(worker.position, self.position)
        self.assertEqual(worker.team, self.team)


class WorkerUpdateFormTest(WorkerFormMixin, TestCase):
    def setUp(self):
        self.worker = Worker.objects.create_user(
            username=self.base_data["username"],
            password=self.base_data["password1"],
            first_name=self.base_data["first_name"],
            last_name=self.base_data["last_name"],
            email=self.base_data["email"],
            position=self.position,
            team=self.team,
        )

    def test_valid_update(self):
        updated_data = self.base_data.copy()
        updated_data["first_name"] = "Updated"
        form = WorkerUpdateForm(data=updated_data, instance=self.worker)
        self.assertTrue(form.is_valid())

    def test_missing_names(self):
        data = self.base_data.copy()
        data["first_name"] = ""
        data["last_name"] = ""
        form = WorkerUpdateForm(data=data, instance=self.worker)
        self.assertFalse(form.is_valid())
        for field in ["first_name", "last_name"]:
            with self.subTest(field=field):
                self.assertIn(field, form.errors)

    def test_worker_updated(self):
        updated_data = self.base_data.copy()
        updated_data.update(
            {
                "first_name": "UpdatedFirstName",
                "last_name": "UpdatedLastName",
                "email": "updated@example.com",
            }
        )
        form = WorkerUpdateForm(data=updated_data, instance=self.worker)
        self.assertTrue(form.is_valid())
        worker = form.save()
        self.assertEqual(worker.first_name, "UpdatedFirstName")
        self.assertEqual(worker.email, "updated@example.com")


class ProjectFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(name="Team X")
        cls.base_data = {
            "name": "Project X",
            "description": "Some project description",
            "deadline": date.today() + timedelta(days=30),
            "teams": [cls.team.id],
        }

    def test_valid_form(self):
        form = ProjectForm(data=self.base_data)
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        data = self.base_data.copy()
        data.pop("name")
        form = ProjectForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_project_created(self):
        form = ProjectForm(data=self.base_data)
        self.assertTrue(form.is_valid())
        project = form.save()
        self.assertIn(self.team, project.teams.all())


class TaskFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.worker = Worker.objects.create_user(username="worker1", password="pass")
        cls.task_type = TaskType.objects.create(name="Feature")
        cls.project = Project.objects.create(name="Proj A", deadline=date.today())
        cls.base_data = {
            "name": "Build feature X",
            "description": "Implement feature X",
            "deadline": date.today(),
            "priority": Task.MEDIUM,
            "task_type": cls.task_type.id,
            "project": cls.project.id,
            "assignees": [cls.worker.id],
        }

    def test_valid_form(self):
        form = TaskForm(data=self.base_data)
        self.assertTrue(form.is_valid())

    def test_missing_fields(self):
        data = self.base_data.copy()
        for field in ["name", "description"]:
            data.pop(field)
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid())
        for field in ["name", "description"]:
            with self.subTest(field=field):
                self.assertIn(field, form.errors)

    def test_task_created(self):
        form = TaskForm(data=self.base_data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.name, self.base_data["name"])
        self.assertIn(self.worker, task.assignees.all())


class NameSearchFormTest(TestCase):
    def test_valid_name_search(self):
        form = NameSearchForm(data={"name": "Test"})
        self.assertTrue(form.is_valid())

    def test_empty_search(self):
        form = NameSearchForm(data={})
        self.assertTrue(form.is_valid())
