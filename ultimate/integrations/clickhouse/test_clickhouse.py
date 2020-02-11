from posthog.api.test.base import BaseTest
from django_clickhouse import migrations
from ultimate.integrations.clickhouse.models import Event

class TestModels(BaseTest):
    def test_something(self):

        event = Event.objects.create(event='user signed up')
        event = Event.objects.create(event='user logged in')
        self.assertEqual(Event.objects.get(event='user signed up').event, 'user signed up')

    def test_meta_object_name(self):
        events = Event.objects.all()
        self.assertEqual(events.model._meta.object_name, 'Event')