from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


from tasks.forms import TaskSearchForm, TaskForm
from tasks.models import Project, Task
from workers.models import Worker


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_workers = Worker.objects.count()
    num_projects = Project.objects.count()
    num_tasks = Task.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_workers": num_workers,
        "num_projects": num_projects,
        "num_tasks": num_tasks,
        "num_visits": num_visits + 1,
    }
    return render(request, "tasks/index.html", context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "task_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        task_type = self.request.GET.get("task_type", "")
        context["search_form"] = TaskSearchForm(initial={
            "name": name,
            "task_type": task_type
        })
        return context

    def get_queryset(self):
        queryset = Task.objects.all().select_related("project")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get("name"):
                queryset = queryset.filter(name__icontains=form.cleaned_data["name"])
            if form.cleaned_data.get("task_type"):
                queryset = queryset.filter(task_type=form.cleaned_data["task_type"])

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Task
    queryset = Task.objects.all().select_related("project")
    form_class = TaskForm
    permission_required = "tasks.add_task"


class TaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    permission_required = "tasks.change_task"


class TaskDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task_list")
    permission_required = "tasks.delete_task"
