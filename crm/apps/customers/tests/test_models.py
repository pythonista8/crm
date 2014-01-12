from django import test
from apps.accounts.models import User, Company
from apps.customers.models import Customer


class CustomersModelsTest(test.TestCase):
    def setUp(self):
        comp = Company.objects.create(name='test')
        user = User.objects.create(email='t@t.com', company=comp)
        self.customer = Customer.objects.create(
            first_name="test", last_name="test", user=user)

    def test_customer(self):
        self.assertEqual(self.customer.first_name, "test")
        self.assertEqual(self.customer.last_name, "test")
        self.assertIsNotNone(self.customer.date_created)
        self.assertIsNotNone(self.customer.date_modified)
        # Check if `date_modified` is changed when object is updated.
        self.customer.save()
        self.assertGreaterEqual(self.customer.date_modified,
                                self.customer.date_created)
