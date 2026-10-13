from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView

from tasks.models import Task
from workers.forms import WorkerSearchForm, WorkerCreationForm, UserRegisterForm, WorkerUpdateForm
from workers.models import Worker
from workers.services.user_service import UserService


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "workers/worker_list.html"
    context_object_name = "worker_list"
    paginate_by = 10

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        first_name = self.request.GET.get("first_name", "")
        position = self.request.GET.get("position", "")
        context["search_form"] = WorkerSearchForm(initial={
            "first_name": first_name,
            "position": position
        })
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.select_related("position")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data["first_name"]:
                queryset = queryset.filter(first_name__icontains=form.cleaned_data["first_name"])
            if form.cleaned_data["position"]:
                queryset = queryset.filter(position=form.cleaned_data["position"])
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()

        completed_qs = Task.objects.filter(assignees=worker, is_completed=True)
        in_progress_qs = Task.objects.filter(assignees=worker, is_completed=False)

        context["num_completed"] = completed_qs.count()
        context["num_in_progress"] = in_progress_qs.count()

        context["completed_list"] = completed_qs.select_related("task_type", "project")
        context["in_progress_list"] = in_progress_qs.select_related("task_type", "project")

        return context


class WorkerCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("workers:worker-list")
    permission_required = "workers.add_worker"


class WorkerUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("workers:worker-list")

    def test_func(self):
        worker = self.get_object()
        return self.request.user == worker or self.request.user.has_perm("workers.change_worker")


class WorkerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Worker
    permission_required = "workers.delete_worker"
    success_url = reverse_lazy("workers:worker-list")


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    user_service = UserService()
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        url = self.request.build_absolute_uri("/")

        self.user_service.register_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
            url=url
        )

        return super().form_valid(form)
