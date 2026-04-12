from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

from accounts.models import CustomUser
from accounts.models import WorkerProfile
from services.models import ServiceRequest


class WorkerRecommendationScore(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	worker = models.OneToOneField(
		WorkerProfile,
		on_delete=models.CASCADE,
		related_name="recommendation_score",
	)
	raw_average_rating = models.DecimalField(max_digits=5, decimal_places=4, default=0)
	total_reviews = models.IntegerField(default=0)
	recommendation_score = models.DecimalField(
		max_digits=6,
		decimal_places=4,
		default=0,
	)
	bayesian_rating = models.DecimalField(
		max_digits=5,
		decimal_places=4,
		default=0,
	)
	average_sentiment_compound = models.DecimalField(
		max_digits=5,
		decimal_places=4,
		default=0,
	)
	sentiment_adjustment = models.DecimalField(max_digits=5, decimal_places=4, default=0)
	average_distance_km = models.DecimalField(max_digits=8, decimal_places=3, default=0)
	distance_component = models.DecimalField(max_digits=6, decimal_places=4, default=0)
	rank_last_updated_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at"]

	def __str__(self):
		return f"RecommendationScore(worker={self.worker_id}, score={self.recommendation_score})"


class WorkerReview(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	request = models.OneToOneField(
		ServiceRequest,
		on_delete=models.CASCADE,
		related_name="review",
		db_column="request_id",
	)
	worker = models.ForeignKey(
		WorkerProfile,
		on_delete=models.CASCADE,
		related_name="reviews",
	)
	reviewer = models.ForeignKey(
		CustomUser,
		on_delete=models.CASCADE,
		related_name="worker_reviews",
		db_column="reviewer_id",
	)
	rating = models.PositiveSmallIntegerField(
		validators=[MinValueValidator(1), MaxValueValidator(5)]
	)
	review_text = models.TextField(blank=True)
	moderation_status = models.CharField(max_length=20, default="APPROVED")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Review(worker={self.worker_id}, rating={self.rating})"
