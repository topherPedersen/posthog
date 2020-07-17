from .base import BaseTest
from posthog.models import Team, Event


class TestTeam(BaseTest):
    def test_event_properties_numerical(self):
        Event.objects.create(team=self.team, event="purchase", distinct_id="x", properties={"total": 2})
        Event.objects.create(team=self.team, event="purchase", distinct_id="x", properties={"total": 554})
        Event.objects.create(
            team=self.team, event="jump", distinct_id="x", properties={"height": 2, "distance": 2, "object": "table"}
        )
        Event.objects.create(
            team=self.team, event="jump", distinct_id="x", properties={"height": 554, "distance": 4, "object": "cat"}
        )
        Event.objects.create(team=self.team, event="jump", distinct_id="x", properties={"height": "9", "object": "dog"})
        Event.objects.create(team=self.team, event="jump", distinct_id="x", properties={"height": "9", "object": "dog"})

        self.assertEqual(set(self.team.event_properties_numeric), {"total", "height", "distance"})
