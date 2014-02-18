from django import test
from apps.accounts.models import Company, User


class CompanyTest(test.TestCase):
    fixtures = ['accounts_models_testdata.json']

    def setUp(self):
        self.company = Company.objects.get(pk=1)

    def test(self):
        print(self.fixtures)


class AccountsModelsTest(test.TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name='Onekloud', website='http://www.onekloud.com',
            street='Petronas Twin Towers', city='Kuala Lumpur', state='WP',
            country='Malaysia')
        self.user = User.objects.create_user(
            'aldash@onekloud.com', password='123', first_name='Aldash',
            last_name='Biibosunov', phone='+123456', company=self.company)

    def test_company(self):
        self.assertEqual(self.company.name, 'Onekloud')
        self.assertIsNotNone(self.company.date_created)
        self.assertTrue(self.company.__str__())

    def test_user(self):
        self.assertEqual(self.user.email, 'aldash@onekloud.com')
        self.assertIsNotNone(self.user.date_created)
        self.assertTrue(self.user.__str__())
        self.assertTrue(self.user.is_trial)
        self.assertFalse(self.user.is_head)
        self.assertEqual(self.user.get_full_name(), 'Aldash Biibosunov')
        self.assertIn(str(self.user.pk), self.user.get_absolute_url())

        # Get short name.
        self.assertEqual(self.user.get_short_name(), 'Aldash')
        self.user.first_name = ''
        self.assertEqual(self.user.get_short_name(), 'aldash')
