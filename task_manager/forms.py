from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Worker, Project, Team, Position, Task, TaskType


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")

    class Meta:
        model = Worker
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        labels = {
            "username": "Username",
            "password1": "Password",
            "password2": "Confirm Password",
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user


class WorkerCreateForm(SignUpForm):
    position = forms.ModelChoiceField(queryset=Position.objects.all(), required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)

    class Meta:
        model = Worker
        fields = SignUpForm.Meta.fields + ["position", "team"]


class WorkerUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True, label="Username")
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    position = forms.ModelChoiceField(queryset=Position.objects.all(), required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)

    class Meta:
        model = Worker
        fields = ["username", "first_name", "last_name", "email", "position", "team"]


class ProjectForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"format": "yyyy-mm-dd", "type": "date"})
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Project
        fields = "__all__"


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"format": "yyyy-mm-dd", "type": "date"})
    )
    task_type = forms.ModelChoiceField(queryset=TaskType.objects.all(), required=False)
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Task
        fields = "__all__"
        exclude = ("is_completed",)


class NameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )
