import datetime

from django import test
from apps.accounts.models import User, Company
from apps.events.models import Event, FollowUp, Meeting


class EventsModelsTest(test.TestCase):
    def setUp(self):
        comp = Company.objects.create(name='test')
        self.user = User.objects.create(email='t@t.com', company=comp)
        kwargs = dict(subject="test", date_created=datetime.datetime.now())
        self.event = Event.objects.create(**kwargs)
        kwargs['user'] = self.user
        self.followup = FollowUp.objects.create(date=datetime.date.today(),
                                                **kwargs)
        now = datetime.datetime.now()
        self.meeting = Meeting.objects.create(date_started=now,
                                              date_ended=now, **kwargs)

    def test_event(self):
        self.assertEqual(self.event.subject, "test")
        self.assertIsNotNone(self.event.date_created)
        self.assertTrue(self.event.__str__())

    def test_followup(self):
        self.assertIsInstance(self.followup, Event)
        self.assertEqual(self.followup.subject, "test")
        self.assertEqual(self.followup.user.pk, self.user.pk)
        self.assertIsNotNone(self.followup.date_created)
        self.assertIsNotNone(self.followup.date)
        self.assertTrue(self.followup.__str__())

    def test_meeting(self):
        self.assertIsInstance(self.meeting, Event)
        self.assertEqual(self.meeting.subject, "test")
        self.assertEqual(self.meeting.user.pk, self.user.pk)
        self.assertIsNotNone(self.meeting.date_created)
        self.assertIsNotNone(self.meeting.date_started)
        self.assertIsNotNone(self.meeting.date_ended)
        self.assertTrue(self.meeting.__str__())
