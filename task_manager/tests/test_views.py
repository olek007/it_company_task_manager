from datetime import date

from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from task_manager.models import Position, Team, Worker, Project, TaskType, Task

User = get_user_model()


class AuthenticatedEnsureMixin:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.password = "strongpass123!"
        cls.username = "AuthUser"
        cls.user = User.objects.create_user(
            username=cls.username, password=cls.password
        )

    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)


class CRUDTestMixin:
    model = None
    base_url_name = ""
    base_template_name = ""
    instance = None
    create_data = {}
    update_data = {}

    def test_list_view(self):
        url = reverse_lazy(f"{self.base_url_name}-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f"{self.base_template_name}_list.html")

    def test_detail_view(self):
        url = reverse_lazy(f"{self.base_url_name}-detail", args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f"{self.base_template_name}_detail.html")

    def test_create_view_get(self):
        url = reverse_lazy(f"{self.base_url_name}-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f"{self.base_template_name}_form.html")

    def test_create_view_post(self):
        url = reverse_lazy(f"{self.base_url_name}-create")
        response = self.client.post(url, self.create_data)
        self.assertEqual(response.status_code, 302)
        filter_fields = {
            key: value
            for key, value in self.create_data.items()
            if key in [field.name for field in self.model._meta.fields]
        }
        is_new_obj_exists = self.model.objects.filter(**filter_fields).exists()
        self.assertTrue(is_new_obj_exists)
        self.assertRedirects(response, reverse_lazy(f"{self.base_url_name}-list"))

    def test_update_view_get(self):
        url = reverse_lazy(f"{self.base_url_name}-update", args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f"{self.base_template_name}_form.html")

    def test_update_view_post(self):
        url = reverse_lazy(f"{self.base_url_name}-update", args=[self.instance.pk])
        response = self.client.post(url, self.update_data)
        self.assertEqual(response.status_code, 302)
        self.instance.refresh_from_db()
        filter_fields = {
            key: value
            for key, value in self.update_data.items()
            if key in [field.name for field in self.model._meta.fields]
        }
        is_obj_updated = self.model.objects.filter(**filter_fields).exists()
        self.assertTrue(is_obj_updated)
        self.assertRedirects(response, reverse(f"{self.base_url_name}-list"))

    def test_delete_view_get(self):
        url = reverse_lazy(f"{self.base_url_name}-delete", args=[self.instance.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, f"{self.base_template_name}_confirm_delete.html"
        )

    def test_delete_view_post(self):
        url = reverse_lazy(f"{self.base_url_name}-delete", args=[self.instance.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.model.objects.filter(pk=self.instance.pk).exists())
        self.assertRedirects(response, reverse_lazy(f"{self.base_url_name}-list"))


class PermissionTestMixin:
    base_url_name = ""
    instance = None

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        actions = ["list", "create", "detail", "update", "delete"]
        for action in actions:
            args = []
            if action in ["detail", "update", "delete"]:
                args = [self.instance.pk]

            url = reverse_lazy(f"{self.base_url_name}-{action}", args=args)
            response = self.client.get(url)
            login_url = "/accounts/login/"
            self.assertRedirects(
                response,
                f"{login_url}?next={url}",
                msg_prefix=f"Unauthenticated access to '{self.base_url_name}-{action}' should redirect.",
            )


class TaskTypeAuthenticatedViewTests(
    AuthenticatedEnsureMixin, CRUDTestMixin, PermissionTestMixin, TestCase
):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.model = TaskType
        cls.base_url_name = "task_manager:task_type"
        cls.base_template_name = "task_manager/task_type"

        cls.instance = TaskType.objects.create(name="Bug")

        cls.create_data = {
            "name": "Manager",
        }
        cls.update_data = {
            "name": "UpdatedName",
        }


class PositionAuthenticatedViewTests(
    AuthenticatedEnsureMixin, CRUDTestMixin, PermissionTestMixin, TestCase
):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.model = Position
        cls.base_url_name = "task_manager:position"
        cls.base_template_name = "task_manager/position"

        cls.instance = Position.objects.create(name="Developer")

        cls.create_data = {
            "name": "QA",
        }
        cls.update_data = {
            "name": "UpdatedName",
        }


class TeamViewAuthenticatedTests(
    AuthenticatedEnsureMixin, CRUDTestMixin, PermissionTestMixin, TestCase
):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.model = Team
        cls.base_url_name = "task_manager:team"
        cls.base_template_name = "task_manager/team"

        cls.instance = Team.objects.create(name="Alpha")

        cls.create_data = {
            "name": "Beta",
        }
        cls.update_data = {
            "name": "UpdatedName",
        }


class WorkerAuthenticatedViewTests(
    AuthenticatedEnsureMixin, CRUDTestMixin, PermissionTestMixin, TestCase
):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.model = Worker
        cls.base_url_name = "task_manager:worker"
        cls.base_template_name = "task_manager/worker"

        cls.position = Position.objects.create(name="Engineer")
        cls.team = Team.objects.create(name="DevOps")
        cls.instance = Worker.objects.create_user(
            username="jdoe",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            email="jdoe@example.com",
            position=cls.position,
            team=cls.team,
        )

        cls.create_data = {
            "username": "asmith",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "asmith@example.com",
            "position": cls.position.pk,
            "team": cls.team.pk,
        }
        cls.update_data = {
            "username": "jdoe",
            "first_name": "Johnny",
            "last_name": "Doe",
            "email": "johnny@example.com",
            "position": cls.position.pk,
            "team": cls.team.pk,
        }


class ProjectAuthenticatedViewTests(
    AuthenticatedEnsureMixin, CRUDTestMixin, PermissionTestMixin, TestCase
):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.model = Project
        cls.base_url_name = "task_manager:project"
        cls.base_template_name = "task_manager/project"

        cls.team = Team.objects.create(name="Team X")
        cls.instance = Project.objects.create(
            name="Launch Rocket", deadline=date.today()
        )
        cls.instance.teams.add(cls.team)

        cls.create_data = {
            "name": "Build AI",
            "description": "Some description",
            "deadline": date.today(),
            "teams": [cls.team.pk],
        }
        cls.update_data = {
            "name": "Updated Project",
            "description": "Updated description",
            "deadline": date.today(),
            "teams": [cls.team.pk],
        }


class TaskAuthenticatedViewTests(
    AuthenticatedEnsureMixin, CRUDTestMixin, PermissionTestMixin, TestCase
):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.model = Task
        cls.base_url_name = "task_manager:task"
        cls.base_template_name = "task_manager/task"

        cls.task_type = TaskType.objects.create(name="Feature")
        cls.project = Project.objects.create(name="Mobile App", deadline=date.today())
        cls.instance = Task.objects.create(
            name="Create UI",
            description="Design login screen",
            deadline=date.today(),
            is_completed=False,
            task_type=cls.task_type,
            project=cls.project,
        )
        cls.instance.assignees.add(cls.user)

        cls.create_data = {
            "name": "Write Tests",
            "description": "Unit tests for task views",
            "deadline": date.today(),
            "is_completed": False,
            "priority": Task.MEDIUM,
            "task_type": cls.task_type.pk,
            "project": cls.project.pk,
            "assignees": [cls.user.pk],
        }
        cls.update_data = {
            "name": "Update UI",
            "description": "Improve colors",
            "deadline": date.today(),
            "priority": Task.HIGH,
            "task_type": cls.task_type.pk,
            "project": cls.project.pk,
            "assignees": [cls.user.pk],
        }
