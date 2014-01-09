from django import test
from django.core.urlresolvers import reverse
from lib.test import setup_view
from apps.accounts.models import User
from apps.companies.models import Company
from apps.companies.forms import CompanyForm
from apps.companies.views import (CompanyList, CompanyCreate, CompanyUpdate,
                                  CompanyContextMixin)


class CompanyContextMixinTest(test.TestCase):
    def setUp(self):
        self.object = CompanyContextMixin()

    def test_attr(self):
        self.assertEqual(self.object.model, Company)

    def test_get_context_data(self):
        self.assertTrue(callable(self.object.get_context_data))


class CompaniesListTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        self.view = setup_view(CompanyList(), self.request)
        user = User.objects.create(email='t@t.com')
        object_list = [Company.objects.create(name="test", user=user)]
        setattr(self.view, 'object_list', object_list)

    def test_get(self):
        resp = self.client.get(reverse('companies:list'))
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, Company)

    def test_get_context_data(self):
        self.ctx = self.view.get_context_data()
        self.assertIn('title', self.ctx)

    def test_get_success_url(self):
        self.assertIsNotNone(self.view.get_success_url())


class CompaniesCreateTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        self.view = setup_view(CompanyCreate(), self.request)
        user = User.objects.create(email='t@t.com')
        object_ = Company.objects.create(name="test", user=user)
        setattr(self.view, 'object', object_)

    def test_get(self):
        resp = self.client.get(reverse('companies:create'))
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, Company)
        self.assertEqual(self.view.form_class, CompanyForm)

    def test_get_context_data(self):
        self.ctx = self.view.get_context_data()
        self.assertIn('title', self.ctx)


class CompaniesUpdateTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        user = User.objects.create(email='t@t.com')
        self.object = Company.objects.create(name="test", user=user)
        self.view = setup_view(CompanyUpdate(), self.request,
                               pk=self.object.pk)
        setattr(self.view, 'object', self.object)

    def test_get(self):
        resp = self.client.get(reverse('companies:edit',
                                       args=[self.object.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, Company)
        self.assertEqual(self.view.form_class, CompanyForm)
        self.assertIsNotNone(self.view.success_message)

    def test_get_context_data(self):
        self.ctx = self.view.get_context_data()
        self.assertIn('title', self.ctx)

    def test_get_success_url(self):
        self.assertIsNotNone(self.view.get_success_url())
