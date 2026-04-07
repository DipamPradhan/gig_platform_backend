from rest_framework import serializers
from accounts.models import WorkerProfile

from .models import (
    ServiceCategory,
    ServiceRequest,
    ServiceRequestBroadcast,
    ServiceRequestEvent,
    ServiceRouteSnapshot,
)


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ("id", "name", "slug", "is_active")


class ServiceRequestSerializer(serializers.ModelSerializer):
    preferred_worker_id = serializers.UUIDField(
        write_only=True,
        required=False,
        allow_null=True,
    )
    assigned_worker_details = serializers.SerializerMethodField(read_only=True)
    requester_details = serializers.SerializerMethodField(read_only=True)
    customer_visible_status = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = ServiceRequest
        fields = (
            "id",
            "requester",
            "requester_details",
            "category",
            "category_name",
            "title",
            "description",
            "request_latitude",
            "request_longitude",
            "request_address",
            "search_radius_km",
            "status",
            "customer_visible_status",
            "preferred_worker_id",
            "assigned_worker",
            "assigned_worker_details",
            "assigned_at",
            "expected_start_at",
            "closed_at",
            "cancellation_reason",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "requester",
            "status",
            "assigned_worker",
            "assigned_at",
            "closed_at",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        preferred_worker_id = attrs.get("preferred_worker_id")
        if not preferred_worker_id:
            return attrs

        worker_profile = WorkerProfile.objects.filter(worker_id=preferred_worker_id).first()
        if not worker_profile:
            raise serializers.ValidationError(
                {"preferred_worker_id": "Selected worker was not found."}
            )

        if worker_profile.verification_status != WorkerProfile.VERIFICATION_STATUS.VERIFIED:
            raise serializers.ValidationError(
                {"preferred_worker_id": "Selected worker is not verified."}
            )

        if worker_profile.availability_status != WorkerProfile.AVAILABILITY_STATUS.ACTIVE:
            raise serializers.ValidationError(
                {"preferred_worker_id": "Selected worker is not currently active."}
            )

        attrs["preferred_worker_profile"] = worker_profile
        return attrs

    def create(self, validated_data):
        validated_data.pop("preferred_worker_id", None)
        validated_data.pop("preferred_worker_profile", None)
        return super().create(validated_data)

    def get_requester_details(self, obj):
        requester = obj.requester
        return {
            "id": str(requester.id),
            "first_name": requester.first_name,
            "last_name": requester.last_name,
            "username": requester.username,
            "phone_number": requester.phone_number,
            "email": requester.email,
        }

    def get_assigned_worker_details(self, obj):
        if not obj.assigned_worker:
            return None

        worker_user = obj.assigned_worker.worker
        return {
            "id": str(obj.assigned_worker.id),
            "worker_id": str(worker_user.id),
            "first_name": worker_user.first_name,
            "last_name": worker_user.last_name,
            "username": worker_user.username,
            "service_category": obj.assigned_worker.service_category,
            "average_rating": obj.assigned_worker.average_rating,
            "total_reviews": obj.assigned_worker.total_reviews,
            "availability_status": obj.assigned_worker.availability_status,
        }

    def get_customer_visible_status(self, obj):
        if (
            obj.status == ServiceRequest.Status.CANCELLED
            and (obj.cancellation_reason or "").lower().startswith("rejected by worker")
        ):
            return "REJECTED"
        return obj.status


class ServiceRequestBroadcastSerializer(serializers.ModelSerializer):
    service_request = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ServiceRequestBroadcast
        fields = (
            "id",
            "request",
            "worker",
            "status",
            "distance_km",
            "ranking_score",
            "expires_at",
            "responded_at",
            "rejection_reason",
            "created_at",
            "service_request",
        )
        read_only_fields = fields

    def get_service_request(self, obj):
        request_obj = obj.request
        requester = request_obj.requester
        return {
            "id": str(request_obj.id),
            "title": request_obj.title,
            "description": request_obj.description,
            "status": request_obj.status,
            "service_category": request_obj.category.name,
            "address": request_obj.request_address,
            "request_latitude": request_obj.request_latitude,
            "request_longitude": request_obj.request_longitude,
            "created_at": request_obj.created_at,
            "customer": {
                "id": str(requester.id),
                "first_name": requester.first_name,
                "last_name": requester.last_name,
                "phone_number": requester.phone_number,
                "email": requester.email,
            },
        }


class ServiceRequestBroadcastActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["accept", "reject"])
    rejection_reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs["action"] == "reject" and not attrs.get("rejection_reason"):
            raise serializers.ValidationError(
                {"rejection_reason": "Rejection reason is required for reject action."}
            )
        return attrs


class WorkerRecommendationResultSerializer(serializers.Serializer):
    worker_id = serializers.UUIDField()
    worker_name = serializers.CharField()
    phone_number = serializers.CharField(allow_null=True)
    username = serializers.CharField(allow_null=True)
    service_category = serializers.CharField()
    skills = serializers.CharField(allow_null=True)
    bio = serializers.CharField(allow_null=True)
    hourly_rate = serializers.DecimalField(max_digits=6, decimal_places=2, allow_null=True)
    total_jobs_completed = serializers.IntegerField()
    total_reviews = serializers.IntegerField()
    user_latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    user_longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    worker_latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    worker_longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    distance_km = serializers.DecimalField(max_digits=8, decimal_places=3)
    bayesian_rating = serializers.DecimalField(max_digits=5, decimal_places=4)
    sentiment_score = serializers.DecimalField(max_digits=6, decimal_places=4)
    final_score = serializers.DecimalField(max_digits=7, decimal_places=4)


class ServiceRequestStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[
            ServiceRequest.Status.ARRIVING,
            ServiceRequest.Status.IN_PROGRESS,
            ServiceRequest.Status.COMPLETED,
            ServiceRequest.Status.CANCELLED,
        ]
    )
    detail = serializers.CharField(required=False, allow_blank=True)


class ServiceRequestCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True, max_length=500)


class ServiceRequestEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequestEvent
        fields = ("id", "request", "event_type", "actor", "detail", "created_at")
        read_only_fields = fields


class ServiceRouteSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRouteSnapshot
        fields = (
            "id",
            "request",
            "origin_latitude",
            "origin_longitude",
            "destination_latitude",
            "destination_longitude",
            "estimated_distance_km",
            "estimated_duration_minutes",
            "route_polyline",
            "map_url",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
