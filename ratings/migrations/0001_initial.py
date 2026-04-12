from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0007_fix_invalid_service_categories"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkerRecommendationScore",
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
                    "recommendation_score",
                    models.DecimalField(decimal_places=4, default=0, max_digits=6),
                ),
                (
                    "bayesian_rating",
                    models.DecimalField(decimal_places=4, default=0, max_digits=5),
                ),
                (
                    "average_sentiment_compound",
                    models.DecimalField(decimal_places=4, default=0, max_digits=5),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "worker",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recommendation_score",
                        to="accounts.workerprofile",
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
    ]