import datetime

from django import test
from apps.accounts.models import User
from django.core.urlresolvers import reverse
from lib.test import setup_view
from apps.events.forms import MeetingForm, FollowUpForm
from apps.events.models import Meeting, FollowUp
from apps.events.views import MeetingUpdate, FollowUpUpdate, EventContextMixin


class IndexTest(test.TestCase):
    def test_get(self):
        resp = self.client.get(reverse('events:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'events/index.html')

    def test_post(self):
        text = "Meet Sam on 15 Dec at 18.30 at Starbucks"
        resp = self.client.post(reverse('events:index'), data=dict(text=text))
        self.assertEqual(resp.status_code, 200)

    def test_post_empty(self):
        resp = self.client.post(reverse('events:index'), data=dict())
        self.assertFormError(resp, 'event_form', 'text', 'This field is required.')

    def test_post_invalid(self):
        resp = self.client.post(reverse('events:index'), data=dict(text=5))
        self.assertFormError(resp, 'event_form', 'text', 'Could not obtain date. Please add.')


class EventContextMixinTest(test.TestCase):
    def setUp(self):
        self.object = EventContextMixin()
        self.object.model = Meeting

    def test_attr(self):
        self.assertIsNone(EventContextMixin.model)
        self.assertEqual(self.object.model, Meeting)
        self.assertIsInstance(EventContextMixin.success_message, str)

    def test_get_context_data(self):
        self.assertTrue(callable(self.object.get_context_data))


class MeetingUpdateTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        self.user = User.objects.create(email='t@t.com')
        now = datetime.datetime.now()
        self.object = Meeting.objects.create(
            user=self.user, subject="Meeting Jay", date_started=now,
            date_ended=now)
        self.view = setup_view(MeetingUpdate(), self.request,
                               pk=self.object.pk)
        setattr(self.view, 'object', self.object)

    def test_get(self):
        resp = self.client.get(reverse('events:edit-meeting',
                                       kwargs={'pk': self.object.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, Meeting)
        self.assertEqual(self.view.form_class, MeetingForm)

    def test_get_success_url(self):
        self.assertIsNotNone(self.view.get_success_url())


class FollowUpUpdateTest(test.TestCase):
    def setUp(self):
        self.request = test.RequestFactory().get('/fake-path')
        self.user = User.objects.create(email='t@t.com')
        today = datetime.date.today()
        self.object = FollowUp.objects.create(
            user=self.user, subject="Call John", date=today)
        self.view = setup_view(FollowUpUpdate(), self.request,
                               pk=self.object.pk)
        setattr(self.view, 'object', self.object)

    def test_get(self):
        resp = self.client.get(reverse('events:edit-followup',
                                       kwargs={'pk': self.object.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_attrs(self):
        self.assertEqual(self.view.model, FollowUp)
        self.assertEqual(self.view.form_class, FollowUpForm)

    def test_get_success_url(self):
        self.assertIsNotNone(self.view.get_success_url())
