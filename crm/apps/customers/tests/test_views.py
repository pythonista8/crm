from django import test
from django.core.urlresolvers import reverse
from lib.test import setup_view
from apps.accounts.models import User
from apps.customers.models import Customer
from apps.customers.forms import CustomerForm
from apps.customers.views import (CustomerList, CustomerCreate, CustomerUpdate,
                                  CustomerContextMixin)


class CustomerContextMixinTest(test.TestCase):
    def setUp(self):
        self.object = CustomerContextMixin()

    def test_attr(self):
        self.assertEqual(self.object.model, Customer)

    def test_get_context_data(self):
        self.assertTrue(callable(self.object.get_context_data))


class CustomersListTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        self.view = setup_view(CustomerList(), self.request)
        user = User.objects.create(email='t@t.com')
        object_list = [Customer.objects.create(first_name="test",
                                               last_name="test",
                                               user=user)]
        setattr(self.view, 'object_list', object_list)

    def test_get(self):
        resp = self.client.get(reverse('customers:list'))
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, Customer)

    def test_get_context_data(self):
        self.ctx = self.view.get_context_data()
        self.assertIn('title', self.ctx)

    def test_get_success_url(self):
        self.assertIsNotNone(self.view.get_success_url())


class CustomersCreateTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        self.view = setup_view(CustomerCreate(), self.request)
        user = User.objects.create(email='t@t.com')
        object_ = Customer.objects.create(first_name="test", last_name="test",
                                          user=user)
        setattr(self.view, 'object', object_)

    def test_get(self):
        resp = self.client.get(reverse('customers:create'))
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, Customer)
        self.assertEqual(self.view.form_class, CustomerForm)

    def test_get_context_data(self):
        self.ctx = self.view.get_context_data()
        self.assertIn('title', self.ctx)


class CustomersUpdateTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        user = User.objects.create(email='t@t.com')
        self.object = Customer.objects.create(first_name="test",
                                              last_name="test",
                                              user=user)
        self.view = setup_view(CustomerUpdate(), self.request,
                               pk=self.object.pk)
        setattr(self.view, 'object', self.object)

    def test_get(self):
        resp = self.client.get(reverse('customers:edit',
                                       args=[self.object.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, Customer)
        self.assertEqual(self.view.form_class, CustomerForm)
        self.assertIsNotNone(self.view.success_message)

    def test_get_context_data(self):
        self.ctx = self.view.get_context_data()
        self.assertIn('title', self.ctx)

    def test_get_success_url(self):
        self.assertIsNotNone(self.view.get_success_url())
