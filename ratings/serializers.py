from rest_framework import serializers

from services.models import ServiceRequest

from .models import WorkerReview


class WorkerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerReview
        fields = (
            "id",
            "request",
            "worker",
            "reviewer",
            "rating",
            "review_text",
            "moderation_status",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "worker",
            "reviewer",
            "created_at",
            "updated_at",
        )


class WorkerReviewReadSerializer(serializers.ModelSerializer):
    reviewer = serializers.SerializerMethodField(read_only=True)
    service_category = serializers.CharField(
        source="request.category.name",
        read_only=True,
    )
    comment = serializers.CharField(source="review_text", read_only=True)

    class Meta:
        model = WorkerReview
        fields = (
            "id",
            "rating",
            "comment",
            "review_text",
            "service_category",
            "reviewer",
            "created_at",
        )

    def get_reviewer(self, obj):
        return {
            "id": str(obj.reviewer_id),
            "first_name": obj.reviewer.first_name,
            "last_name": obj.reviewer.last_name,
            "username": obj.reviewer.username,
        }


class WorkerReviewCreateSerializer(serializers.Serializer):
    request = serializers.UUIDField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    review_text = serializers.CharField(required=False, allow_blank=True, max_length=2000)

    def validate(self, attrs):
        user = self.context["request"].user
        request_id = attrs["request"]

        service_request = ServiceRequest.objects.filter(id=request_id, requester=user).first()
        if not service_request:
            raise serializers.ValidationError({"request": "Service request not found."})

        if service_request.status != ServiceRequest.Status.COMPLETED:
            raise serializers.ValidationError(
                {"request": "You can only review completed service requests."}
            )

        if not service_request.assigned_worker_id:
            raise serializers.ValidationError(
                {"request": "Cannot review a request without an assigned worker."}
            )

        if hasattr(service_request, "review"):
            raise serializers.ValidationError(
                {"request": "A review already exists for this service request."}
            )

        attrs["service_request_obj"] = service_request
        return attrs
