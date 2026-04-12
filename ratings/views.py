from django.db.models import Avg, Count
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ratings.algorithms.sentiment import calculate_sentiment_compound
from services.algorithms.ranking import bayesian_rating

from .models import WorkerRecommendationScore, WorkerReview
from .serializers import (
	WorkerReviewCreateSerializer,
	WorkerReviewReadSerializer,
)


class ReviewListCreateView(generics.GenericAPIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		worker_id = request.query_params.get("worker_id")
		queryset = WorkerReview.objects.select_related(
			"reviewer",
			"worker",
			"request",
			"request__category",
		)
		if worker_id:
			queryset = queryset.filter(worker__worker_id=worker_id)

		serializer = WorkerReviewReadSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		serializer = WorkerReviewCreateSerializer(
			data=request.data,
			context={"request": request},
		)
		serializer.is_valid(raise_exception=True)

		service_request = serializer.validated_data["service_request_obj"]
		rating = serializer.validated_data["rating"]
		review_text = serializer.validated_data.get("review_text", "")

		review = WorkerReview.objects.create(
			request=service_request,
			worker=service_request.assigned_worker,
			reviewer=request.user,
			rating=rating,
			review_text=review_text,
		)

		worker = service_request.assigned_worker
		aggregates = WorkerReview.objects.filter(worker=worker).aggregate(
			avg_rating=Avg("rating"),
			count_reviews=Count("id"),
		)
		reviews_queryset = WorkerReview.objects.filter(worker=worker).only("review_text")

		avg_rating = float(aggregates["avg_rating"] or 0)
		review_count = int(aggregates["count_reviews"] or 0)
		sentiment_values = [
			calculate_sentiment_compound(item.review_text)
			for item in reviews_queryset
		]
		avg_sentiment = (
			round(sum(sentiment_values) / len(sentiment_values), 4)
			if sentiment_values
			else 0
		)

		worker.average_rating = avg_rating
		worker.total_reviews = review_count
		worker.save(update_fields=["average_rating", "total_reviews", "updated_at"])

		score_obj, _ = WorkerRecommendationScore.objects.get_or_create(worker=worker)
		score_obj.raw_average_rating = avg_rating
		score_obj.total_reviews = review_count
		score_obj.bayesian_rating = bayesian_rating(avg_rating, review_count)
		score_obj.average_sentiment_compound = avg_sentiment
		score_obj.sentiment_adjustment = avg_sentiment
		score_obj.recommendation_score = score_obj.bayesian_rating
		score_obj.save(
			update_fields=[
				"raw_average_rating",
				"total_reviews",
				"bayesian_rating",
				"average_sentiment_compound",
				"sentiment_adjustment",
				"recommendation_score",
				"rank_last_updated_at",
				"updated_at",
			]
		)

		return Response(
			WorkerReviewReadSerializer(review).data,
			status=status.HTTP_201_CREATED,
		)


class SentimentListView(generics.GenericAPIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		worker_id = request.query_params.get("worker_id")
		queryset = WorkerReview.objects.select_related("worker")
		if worker_id:
			queryset = queryset.filter(worker__worker_id=worker_id)

		payload = [
			{
				"review_id": str(review.id),
				"worker_id": str(review.worker.worker_id),
				"sentiment_compound": calculate_sentiment_compound(review.review_text),
				"created_at": review.created_at,
			}
			for review in queryset
		]
		return Response(payload, status=status.HTTP_200_OK)
