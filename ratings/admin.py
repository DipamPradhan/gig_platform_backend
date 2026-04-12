from django.contrib import admin
from .models import WorkerReview, ReviewSentiment, WorkerRecommendationScore


@admin.register(WorkerReview)
class WorkerReviewAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"request",
		"reviewer",
		"worker",
		"rating",
		"moderation_status",
		"created_at",
	)
	list_filter = ("rating", "moderation_status")
	search_fields = ("reviewer__email", "worker__worker__email")


@admin.register(ReviewSentiment)
class ReviewSentimentAdmin(admin.ModelAdmin):
	list_display = ("id", "review", "label", "compound_score", "confidence", "processed_at")
	list_filter = ("label",)


@admin.register(WorkerRecommendationScore)
class WorkerRecommendationScoreAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"worker",
		"bayesian_rating",
		"average_sentiment_compound",
		"distance_component",
		"recommendation_score",
		"rank_last_updated_at",
	)
	search_fields = ("worker__worker__email",)
