from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_fix_invalid_service_categories"),
        ("ratings", "0001_initial"),
        ("services", "0002_remove_servicerequest_budget_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkerReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.PositiveSmallIntegerField(),
                ),
                (
                    "review_text",
                    models.TextField(blank=True),
                ),
                (
                    "sentiment_compound",
                    models.DecimalField(decimal_places=4, default=0, max_digits=6),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="worker_reviews",
                        to="accounts.customuser",
                    ),
                ),
                (
                    "service_request",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="review",
                        to="services.servicerequest",
                    ),
                ),
                (
                    "worker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="accounts.workerprofile",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
