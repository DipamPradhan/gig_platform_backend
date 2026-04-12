from rest_framework import serializers

from .models import WorkerReview, ReviewSentiment, WorkerRecommendationScore


class WorkerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerReview
        fields = (
            "id",
            "request",
            "reviewer",
            "worker",
            "rating",
            "review_text",
            "moderation_status",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "reviewer",
            "worker",
            "moderation_status",
            "created_at",
            "updated_at",
        )


class ReviewSentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSentiment
        fields = (
            "id",
            "review",
            "label",
            "compound_score",
            "confidence",
            "metadata",
            "processed_at",
        )
        read_only_fields = fields


class WorkerRecommendationScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerRecommendationScore
        fields = (
            "id",
            "worker",
            "raw_average_rating",
            "total_reviews",
            "bayesian_rating",
            "average_sentiment_compound",
            "sentiment_adjustment",
            "average_distance_km",
            "distance_component",
            "recommendation_score",
            "rank_last_updated_at",
        )
        read_only_fields = fields
