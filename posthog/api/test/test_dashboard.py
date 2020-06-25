from .base import BaseTest, TransactionBaseTest
from posthog.models import Dashboard, Filter, DashboardItem
from posthog.api.action import calculate_trends
from posthog.decorators import TRENDS_ENDPOINT
from posthog.tasks.update_cache import update_cache
from django.core.cache import cache
import json


class TestDashboard(TransactionBaseTest):
    TESTS_API = True

    def test_token_auth(self):
        self.client.logout()
        dashboard = Dashboard.objects.create(
            team=self.team, share_token="testtoken", name="public dashboard"
        )
        test_no_token = self.client.get("/api/dashboard/%s/" % (dashboard.pk))
        self.assertEqual(test_no_token.status_code, 403)
        response = self.client.get(
            "/api/dashboard/%s/?share_token=testtoken" % (dashboard.pk)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "public dashboard")

    def test_shared_dashboard(self):
        self.client.logout()
        dashboard = Dashboard.objects.create(
            team=self.team, share_token="testtoken", name="public dashboard"
        )
        response = self.client.get("/shared_dashboard/testtoken")
        self.assertIn("bla", response)

    def test_share_dashboard(self):
        dashboard = Dashboard.objects.create(team=self.team, name="dashboard")
        response = self.client.patch(
            "/api/dashboard/%s/" % dashboard.pk,
            {"name": "dashboard 2", "is_shared": True},
            content_type="application/json",
        )
        dashboard = Dashboard.objects.get(pk=dashboard.pk)
        self.assertIsNotNone(dashboard.share_token)

    def test_return_results(self):
        dashboard = Dashboard.objects.create(team=self.team, name="dashboard")
        filter_dict = {
            "events": [{"id": "$pageview"}],
            "properties": [{"key": "$browser", "value": "Mac OS X"}],
        }

        item = DashboardItem.objects.create(
            dashboard=dashboard,
            filters=Filter(data=filter_dict).to_dict(),
            team=self.team,
        )
        DashboardItem.objects.create(
            dashboard=dashboard,
            filters=Filter(data=filter_dict).to_dict(),
            team=self.team,
        )
        response = self.client.get("/api/dashboard/%s/" % dashboard.pk).json()
        self.assertEqual(response["items"][0]["result"], None)
        # cache results
        self.client.get(
            "/api/action/trends/?events=%s&properties=%s"
            % (json.dumps(filter_dict["events"]), json.dumps(filter_dict["properties"]))
        )

        with self.assertNumQueries(5):
            response = self.client.get("/api/dashboard/%s/" % dashboard.pk).json()
        self.assertEqual(response["items"][0]["result"][0]["count"], 0)