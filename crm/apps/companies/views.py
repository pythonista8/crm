from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from apps.companies.models import Company
from apps.companies.forms import CompanyForm


class CompanyContextMixin(object):
    model = Company

    def get_context_data(self, **kwargs):
        ctx = super(CompanyContextMixin, self).get_context_data(**kwargs)
        ctx['title_icon'] = 'building-o'
        return ctx


class CompanyList(CompanyContextMixin, ListView):
    paginate_by = 16

    def get_context_data(self, **kwargs):
        ctx = super(CompanyList, self).get_context_data(**kwargs)
        ctx['title'] = Company._meta.verbose_name_plural.title()
        ctx['verbose_name'] = Company._meta.verbose_name
        return ctx

    def get_success_url(self):
        return reverse('companies:list')


class CompanyCreate(CompanyContextMixin, SuccessMessageMixin, CreateView):
    form_class = CompanyForm
    success_message = "Successfully created"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CompanyCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(CompanyCreate, self).get_context_data(**kwargs)
        ctx['title'] = "Create new {}".format(Company._meta.verbose_name)
        return ctx


class CompanyUpdate(CompanyContextMixin, SuccessMessageMixin, UpdateView):
    form_class = CompanyForm
    success_message = "Successfully updated"

    def get_context_data(self, **kwargs):
        ctx = super(CompanyUpdate, self).get_context_data(**kwargs)
        ctx['title'] = "Edit {}".format(Company._meta.verbose_name)
        return ctx

    def get_success_url(self):
        object_ = self.get_object()
        return reverse('companies:edit', kwargs={'pk': object_.pk})
