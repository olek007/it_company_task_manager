from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from task_manager.models import TaskType, Position, Team, Worker, Project, Task
from task_manager.utilities import Orderings

User = get_user_model()


class BaseModelTestMixin:
    model = None
    name_field = "name"
    test_objects_names = ["Bravo", "Zulu", "Alfa"]
    has_deadline_field = False
    ordering = Orderings.NAME_ASC

    @classmethod
    def setUpTestData(cls):
        cls._instances = []

        for i, name in enumerate(cls.test_objects_names):
            object_data = {cls.name_field: name}
            if cls.has_deadline_field:
                object_data["deadline"] = date.today() + timedelta(days=i)
            obj = cls.model.objects.create(**object_data)
            cls._instances.append(obj)

    def test_create_objects(self):
        self.assertEqual(self.model.objects.count(), len(self.test_objects_names))

    def test_str_returns_name_field(self):
        test_value = "Test Name"
        object_data = {self.name_field: test_value}
        if self.has_deadline_field:
            object_data["deadline"] = date.today()
        instance = self.model.objects.create(**object_data)
        self.assertEqual(str(instance), test_value)

    def test_ordering(self):
        actual = list(self.model.objects.all())
        ordering_field, ordering_order = self.ordering.split("_")
        expected = sorted(
            self._instances,
            key=lambda x: getattr(x, ordering_field),
            reverse="desc" in ordering_order,
        )
        self.assertEqual(actual, expected)


class TaskTypeModelBasicTests(BaseModelTestMixin, TestCase):
    model = TaskType
    ordering = Orderings.NAME_ASC


class PositionModelBasicTests(BaseModelTestMixin, TestCase):
    model = Position
    ordering = Orderings.NAME_ASC


class TeamModelBasicTests(BaseModelTestMixin, TestCase):
    model = Team
    ordering = Orderings.NAME_ASC


class WorkerModelBasicTests(BaseModelTestMixin, TestCase):
    model = Worker
    name_field = "username"
    ordering = Orderings.USERNAME_ASC


class WorkerModelAdditionalTests(TestCase):
    def test_str_returns_username_and_names(self):
        worker = Worker.objects.create_user(
            username="john_doe", first_name="John", last_name="Doe"
        )
        self.assertEqual(str(worker), "john_doe John Doe")

    def test_ordering_by_username(self):
        usernames = ["Bravo", "Zulu", "Alfa"]
        for username in usernames:
            Worker.objects.create_user(username=username)
        ordered = list(Worker.objects.all().values_list("username", flat=True))
        self.assertEqual(ordered, sorted(usernames))

    def test_position_nullable(self):
        worker = User.objects.create_user(username="john_doe")
        self.assertIsNone(worker.position)

    def test_team_nullable(self):
        worker = User.objects.create_user(username="john_doe")
        self.assertIsNone(worker.team)


class ProjectModelBasicTests(BaseModelTestMixin, TestCase):
    model = Project
    has_deadline_field = True
    ordering = Orderings.DEADLINE_DESC


class TaskModelBasicTests(BaseModelTestMixin, TestCase):
    model = Task
    has_deadline_field = True
    ordering = Orderings.DEADLINE_DESC


class TaskModelAdditionalTests(TestCase):
    def test_assignees_many_to_many(self):
        worker1 = User.objects.create_user(username="worker1")
        worker2 = User.objects.create_user(username="worker2")
        task = Task.objects.create(
            name="Task1",
            deadline=date.today(),
            priority=Task.MEDIUM,
        )
        task.assignees.set([worker1, worker2])
        self.assertEqual(set(task.assignees.all()), {worker1, worker2})

    def test_default_priority_is_medium(self):
        task = Task.objects.create(name="Task1", deadline=date.today())
        self.assertEqual(task.priority, Task.MEDIUM)

    def test_default_is_completed_is_false(self):
        task = Task.objects.create(name="Task1", deadline=date.today())
        self.assertEqual(task.is_completed, False)

    def test_task_type_nullable(self):
        task = Task.objects.create(name="Task1", deadline=date.today())
        self.assertIsNone(task.task_type)

    def test_project_nullable(self):
        task = Task.objects.create(name="Task1", deadline=date.today())
        self.assertIsNone(task.project)

    def test_ordering_by_is_completed_deadline_desc_priority(self):
        def date_offset(days_offset):
            return date.today() + timedelta(days=days_offset)

        tasks_data = [
            ("Alfa", date_offset(3), False, Task.URGENT),
            ("Bravo", date_offset(3), False, Task.LOW),
            ("Charlie", date_offset(3), False, Task.MEDIUM),
            ("Delta", date_offset(2), False, Task.URGENT),
            ("Echo", date_offset(2), False, Task.HIGH),
            ("Yankee", date_offset(5), True, Task.URGENT),
            ("Zulu", date_offset(4), True, Task.URGENT),
        ]

        for name, deadline, is_completed, priority in tasks_data:
            Task.objects.create(
                name=name,
                deadline=deadline,
                is_completed=is_completed,
                priority=priority,
            )

        expected_order = [
            ("Alfa", False, date_offset(3), Task.URGENT),
            ("Charlie", False, date_offset(3), Task.MEDIUM),
            ("Bravo", False, date_offset(3), Task.LOW),
            ("Delta", False, date_offset(2), Task.URGENT),
            ("Echo", False, date_offset(2), Task.HIGH),
            ("Yankee", True, date_offset(5), Task.URGENT),
            ("Zulu", True, date_offset(4), Task.URGENT),
        ]

        actual = Task.objects.all()

        for task, expected in zip(actual, expected_order):
            self.assertEqual(
                (task.name, task.is_completed, task.deadline, task.priority), expected
            )
