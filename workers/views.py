from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView

from tasks.models import Task
from workers.forms import WorkerSearchForm, WorkerCreationForm, UserRegisterForm
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
        queryset = get_user_model().objects.all()
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

        context["num_completed"] = Task.objects.filter(assignees=worker, is_completed=True).count()
        context["num_in_progress"] = Task.objects.filter(assignees=worker, is_completed=False).count()
        context["completed_list"] = Task.objects.filter(assignees=worker, is_completed=True)
        context["in_progress_list"] = Task.objects.filter(assignees=worker, is_completed=False)

        return context


class WorkerCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("workers:worker-list")
    permission_required = "workers.add_worker"


class WorkerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerCreationForm
    permission_required = "workers.change_worker"
    success_url = reverse_lazy("workers:worker-list")


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
