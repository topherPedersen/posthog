# Generated by Django 3.0.7 on 2020-06-29 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("posthog", "0067_team_updated_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="Annotation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.CharField(blank=True, max_length=400, null=True)),
                ("created_at", models.DateTimeField(null=True, blank=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "creation_type",
                    models.CharField(
                        choices=[("USR", "User"), ("GIT", "Github")],
                        default="USR",
                        max_length=3,
                    ),
                ),
                ("apply_all", models.BooleanField(default=False)),
                ("deleted", models.BooleanField(default=False)),
                ("date_marker", models.DateTimeField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "dashboard_item",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="posthog.DashboardItem",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="posthog.Team"
                    ),
                ),
            ],
        ),
    ]
