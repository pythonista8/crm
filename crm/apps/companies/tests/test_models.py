from django import test
from apps.accounts.models import User
from apps.companies.models import Company


class CompaniesModelsTestCase(test.TestCase):
    def setUp(self):
        self.user = User.objects.create(email='t@t.com')
        self.company = Company.objects.create(name='test', user=self.user)

    def test_company(self):
        self.assertIsNotNone(self.company.date_created)
        self.assertIsNotNone(self.company.date_modified)
        self.assertEqual(self.company.__str__(), "test")
        # Check if `date_modified` is changed when object is updated.
        self.company.save()
        self.assertGreaterEqual(self.company.date_modified,
                                self.company.date_created)
