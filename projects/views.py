from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import generic

from projects.models import Project
from projects.forms import ProjectSearchForm, ProjectForm
from tasks.models import Task


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "project_list"
    paginate_by = 10

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProjectSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Project.objects.all()
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        context["num_completed"] = Task.objects.filter(project=project, is_completed=True).count()
        context["num_in_progress"] = Task.objects.filter(project=project, is_completed=False).count()
        context["completed_list"] = Task.objects.filter(project=project, is_completed=True)
        context["in_progress_list"] = Task.objects.filter(project=project, is_completed=False)

        return context


class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    permission_required = "projects.add_project"
class ProjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    permission_required = "projects.change_project"

class ProjectDeleteView(LoginRequiredMixin,PermissionRequiredMixin, generic.DeleteView):
    model = Project
    success_url = "projects:project_list"
    permission_required = "projects.delete_project"
